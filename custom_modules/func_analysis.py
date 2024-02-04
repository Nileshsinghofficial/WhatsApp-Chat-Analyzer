import emoji
import collections as c
import pandas as pd

# for visualization
import plotly.express as px
import matplotlib.pyplot as plt

# word cloud
from wordcloud import WordCloud, STOPWORDS


def authors_name(data):
    """
        It returns the name of participants in chat. 
    """
    authors = data.Author.unique().tolist()
    return [name for name in authors if name != None]


def extract_emojis(s):
    """
        This function is used to calculate emojis in text and return in a list.
    """
    return [c for c in s if c in emoji.EMOJI_DATA]


def stats(data, word=None):
    """
        This function takes input as data and return number of messages and total emojis used in chat.
    """
    total_messages = data.shape[0]
    media_messages = data[data['Message'] == '<Media omitted>'].shape[0]
    emojis = sum(data['emoji'].str.len())
    stats_info = "Total Messages 💬: {} \n Total Media 🎬: {} \n Total Emoji's 😂: {}".format(total_messages, media_messages, emojis)

    if word:
        word_count = sum(data['Message'].apply(lambda message: 1 if word.lower() in message.lower() else 0))
        stats_info += "\n Total '{}' mentions: {}".format(word, word_count)

    return stats_info

def popular_emoji(data):
    """
        This function returns the list of emoji's with it's frequency.
    """
    total_emojis_list = list([a for b in data.emoji for a in b])
    emoji_dict = dict(c.Counter(total_emojis_list))
    emoji_list = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    return emoji_list


def visualize_emoji(data):
    """
        This function is used to make pie chart of popular emoji's.
    """
    emoji_df = pd.DataFrame(popular_emoji(data), columns=['emoji', 'count'])
    
    fig = px.pie(emoji_df, values='count', names='emoji', color_discrete_map="identity", title='Emoji Distribution')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    # fig.show()
    return fig

def word_cloud(df):
    """
        This function is used to generate word cloud using dataframe.
    """
    df = df[df['Message'] != '<Media omitted>']
    df = df[df['Message'] != 'This message was deleted']
    words = ' '.join(df['Message'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    # To stop article, punctuations
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    
    # plt.figure(figsize=(45,8))
    fig = plt.figure()
    ax = fig.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig
    

def active_date(data):
    """
        This function is used to generate horizontal bar graph between date and 
        number of messages dataframe.
    """
    fig, ax = plt.subplots()
    ax = data['Date'].value_counts().head(10).plot.barh()
    ax.set_title('Top 10 active date')
    ax.set_xlabel('Number of Messages')
    ax.set_ylabel('Date')
    plt.tight_layout()
    return fig
    
def active_time(data):
    """
    This function generate horizontal bar graph between time and number of messages.

    Parameters
    ----------
    data : Dataframe
        With this data graph is generated.

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots()
    ax = data['Time'].value_counts().head(10).plot.barh()
    ax.set_title('Top 10 active time')
    ax.set_xlabel('Number of messages')
    ax.set_ylabel('Time')
    plt.tight_layout()
    return fig

def day_wise_count(data):
    """
    This function generate a line polar plot.

    Parameters
    ----------
    data : DataFrame
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    day_df = pd.DataFrame(data["Message"])
    day_df['day_of_date'] = data['Date'].dt.weekday
    day_df['day_of_date'] = day_df["day_of_date"].apply(lambda d: days[d])
    day_df["messagecount"] = 1
    
    day = day_df.groupby("day_of_date").sum()
    day.reset_index(inplace=True)
    
    fig = px.line_polar(day, r='messagecount', theta='day_of_date', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        )),
    showlegend=False
    )
    # fig.show()
    return fig

def num_messages(data):
    """
    This function generates the line plot of number of messages on monthly basis.

    Parameters
    ----------
    data : DataFrame
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    data.loc[:, 'MessageCount'] = 1
    date_df = data.groupby("Date").sum()
    date_df.reset_index(inplace=True)
    fig = px.line(date_df, x="Date", y="MessageCount")
    fig.update_xaxes(nticks=20)
    # fig.show()
    return fig

def chatter(data):
    try:
        # Fill null or missing author names with a placeholder (e.g., "Unknown")
        data['Author'].fillna('Unknown', inplace=True)

        # For messages with no author, assign a default author name ("Unknown")
        data.loc[data['Author'].isnull(), 'Author'] = 'Unknown'

        # Sum messages for each author
        auth_counts = data.groupby("Author")["MessageCount"].sum().reset_index()

        # Sorting by the count of messages
        auth_counts = auth_counts.sort_values(by="MessageCount", ascending=False)

        # Create bar plot
        fig = px.bar(auth_counts, y="Author", x="MessageCount", color='Author', orientation="h",
                     color_discrete_sequence=["red", "green", "blue", "goldenrod", "magenta"],
                     title='Number of messages corresponding to author'
                    )
        return fig
    except Exception as e:
        print("Error in chatter function:", str(e))
        raise e


