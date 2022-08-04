mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"danil1994b@yande.ru\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml