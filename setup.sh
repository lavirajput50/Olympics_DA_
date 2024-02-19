mkdir -p ~/.streamlit/
echo "\
[server]\n\
port=$PORT\n\
headless=true\n\
\n\
" >~/.streamlit/credentials.toml