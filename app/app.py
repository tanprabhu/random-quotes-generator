import json, random, html
from pathlib import Path 
import streamlit.components.v1 as components

import streamlit as st

DATA_PATH = Path("data/quotes_normalized.json")

@st.cache_data
def load_quotes(path:Path):
  if not path.exists():
    st.error(f"Quotes file not found:{path}")
    st.stop()

  with path.open("r", encoding="utf-8") as f:
    return json.load(f)
  
def get_all_tags(quotes):
  tags=set()
  for q in quotes:
    for t in q.get("tags",[]):
      tags.add(t)
  return sorted(tags)

def filter_using_tags(quotes, selected_tags):
   if not selected_tags:
      return quotes
   
   return[
      q for q in quotes
      if set(selected_tags).issubset(set(q.get("tags",[])))
   ]


def get_random_quote(quotes):
  return random.choice(quotes)


def quote_card(quote):
    text = html.escape(quote["text"])
    author = html.escape(quote["author"])

    tags_html = "".join(
        f"<span class='tag'>{html.escape(tag)}</span>"
        for tag in quote.get("tags", [])
    )

    html_code = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            background: transparent;
            color: white;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        .card {{
            background-color: rgba(255,255,255,0.04);
            padding: 2.5rem;
            border-radius: 24px;
            max-width: 700px;
            margin: 2rem auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }}

        .quote {{
            font-size: 1.25rem;
            line-height: 1.75;
            font-weight: 500;
            min-height: 6rem;
        }}

        .author {{
            margin-top: 1.8rem;
            font-size: 0.9rem;
            opacity: 0.7;
            font-weight: 600;
        }}

        .tags {{
            margin-top: 1.4rem;
            text-align: center;
        }}

        .tag {{
            display: inline-block;
            padding: 0.35rem 0.7rem;
            margin: 0.25rem;
            border-radius: 999px;
            background-color: rgba(255,255,255,0.08);
            font-size: 0.75rem;
        }}
    </style>
    </head>

    <body>
        <div class="card">
            <div id="quote" class="quote"></div>
            <div class="author">— {author}</div>
            <div class="tags">{tags_html}</div>
        </div>

        <script>
            const text = `{text}`;
            const el = document.getElementById("quote");
            let i = 0;

            function typeChar() {{
                if (i < text.length) {{
                    el.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(typeChar, 20);
                }}
            }}

            typeChar();
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=360)



def main():

  st.set_page_config(
    page_title="Random Quote Generator",
    layout="centered",
  )

  st.title("Random Quote Generator")

  quotes = load_quotes(DATA_PATH)

  if "quote_index" not in st.session_state:
    st.session_state["quote_index"] = 0
  if "active_tags" not in st.session_state:
      st.session_state["active_tags"] = []

  all_tags = get_all_tags(quotes)

  with st.sidebar:
        st.title("Filters")

        selected_tags = st.multiselect(
            "Filter by tags",
            options=all_tags,
        )

        st.divider()
        st.caption("Quotes update only from pre-scraped data.")

  # Reset carousel when tags change 
  if selected_tags != st.session_state["active_tags"]:
        st.session_state["active_tags"] = selected_tags
        st.session_state["quote_index"] = 0

  # filter quotes
  filtered_quotes = filter_using_tags(quotes, selected_tags)

  
  if not filtered_quotes:
        st.warning("No quotes match the selected tags.")
        st.stop()

  st.session_state["quote_index"] %= len(filtered_quotes)
  current_quote = filtered_quotes[st.session_state["quote_index"]]
 
  quote_card(current_quote)

  st.divider()

  #  actions
  col1, col2 = st.columns(2)

  with col1:
      if st.button("← Previous", use_container_width=True):
          st.session_state["quote_index"] -=1
          st.rerun()

  with col2:
      if st.button("Next →", use_container_width=True):
          st.session_state["quote_index"] +=1
          st.rerun()



if __name__ == "__main__":
   main()