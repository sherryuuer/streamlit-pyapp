import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('Stocking GAFA')

st.sidebar.write("""
### GAFA stocking
Set the days of the datas.
Select DAYS:
""")

days = st.sidebar.slider('days', 1, 50, 20)

st.write(f"""
### The last **{days}days's** GAFA stocking datas.
""")


@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df


try:
    st.sidebar.write("""
    ## Stocking Range:
    """)
    ymin, ymax = st.sidebar.slider(
        'Set the range:',
        0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        'Select companies:',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('At least one company should be selected.')
    else:
        data = df.loc[companies]
        st.write("### (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(
        "Something goes wrong!"
    )
    st.write(e)
