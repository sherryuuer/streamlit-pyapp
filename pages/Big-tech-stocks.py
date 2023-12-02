import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('Big tech Stocking GAFAM 🚀')

st.sidebar.write("""
### GAFA stocking
Set the days of the datas.
Select DAYS:
""")

days = st.sidebar.slider('days', 1, 50, 20)

"""
### **Tech Trends:**
Keeping an eye on these tech behemoths means staying informed about their constant innovations. Whether it's Facebook's foray into virtual reality with Oculus, Amazon's advancements in drone delivery, Apple's exploration of augmented reality, Google's developments in AI and self-driving cars, or Microsoft's strides in cloud computing and gaming, the tech landscape is continually evolving.

### **Stock Prices:**
Let's take a glance at their current stock prices:

- **Facebook (Meta Platforms, Inc.):** [FB](https://www.marketwatch.com/investing/stock/fb)
- **Amazon:** [AMZN](https://www.marketwatch.com/investing/stock/amzn)
- **Apple:** [AAPL](https://www.marketwatch.com/investing/stock/aapl)
- **Google (Alphabet Inc.):** [GOOGL](https://www.marketwatch.com/investing/stock/googl)
- **Microsoft:** [MSFT](https://www.marketwatch.com/investing/stock/msft)

These stocks reflect the dynamic nature of the tech industry and the global economy, providing a snapshot of these companies' market performance.

"""

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
        0.0, 2000.0, (0.0, 2000.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'amazon': 'AMZN'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        'Select companies:',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple', 'microsoft']
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
                y=alt.Y("Stock Prices(USD):Q", stack=None,
                        scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(
        "Something goes wrong!"
    )
    st.write(e)
