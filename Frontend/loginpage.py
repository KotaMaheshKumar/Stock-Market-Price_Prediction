# import loginpage as st
# import streamlit as st
# import sqlite3
# import hashlib
# import pandas as pd
# import numpy as np
# import time

# class DatabaseManager:
#     """Manages SQLite operations for custom credentials."""
#     def __init__(self, dbname="users.db"):
#         self.db_name = dbname
#         self.init_db()

#     def get_connection(self):
#         return sqlite3.connect(self.db_name)

#     def init_db(self):
#         with self.get_connection() as conn:
#             conn.execute("""
#                 CREATE TABLE IF NOT EXISTS users (
#                     username TEXT PRIMARY KEY,
#                     email TEXT UNIQUE,
#                     password_hash TEXT
#                 )
#             """)
#             conn.commit()

#     def hash_password(self, password: str) -> str:
#         return hashlib.sha256(password.encode()).hexdigest()

#     def create_user(self, username, email, password) -> bool:
#         try:
#             with self.get_connection() as conn:
#                 pw_hash = self.hash_password(password)
#                 conn.execute(
#                     "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
#                     (username, email, pw_hash)
#                 )
#                 conn.commit()
#             return True
#         except sqlite3.IntegrityError:
#             return False  # Username or Email already exists

#     def verify_user(self, username, password) -> bool:
#         with self.get_connection() as conn:
#             pw_hash = self.hash_password(password)
#             cursor = conn.execute(
#                 "SELECT * FROM users WHERE username = ? AND password_hash = ?",
#                 (username, pw_hash)
#             )
#             return cursor.fetchone() is not None


# class SaaSApplication:
#     def __init__(self):
#         self.setup_page_config()
#         self.db = DatabaseManager()
#         #self.init_session_state()

#     def setup_page_config(self):
#         st.set_page_config(
#             page_title="SaaSify Platform",
#             page_icon="🚀",
#             layout="centered",
#             initial_sidebar_state="collapsed"
#         )

#     # def init_session_state(self):
#     #     # Native Streamlit OIDC Auth check state
#     #     if st.user.is_logged_in:
#     #         st.session_state.logged_in = True
#     #         st.session_state.username = st.user.get("name", st.user.get("email", "OAuth User"))
        
#     #     # Fallback tracking for custom SQLite login flow
#     #     if "logged_in" not in st.session_state:
#     #         st.session_state.logged_in = False
#     #     if "username" not in st.session_state:
#     #         st.session_state.username = ""

#     def handle_logout(self):
#         st.session_state.logged_in = False
#         st.session_state.username = ""
#         if st.user.is_logged_in:
#             st.logout()  # Triggers Streamlit native identity cookie clearance
#         st.rerun()

#     def render_sidebar(self) -> str:
#         st.sidebar.title("Navigation")
#         st.session_state['logged_in'] = False
#         st.session_state['username'] = ""
#         if not st.session_state.logged_in:
#             page = st.sidebar.radio("Go to", ["Home", "Sign In / Sign Up"])
#         else:
#             page = st.sidebar.radio("Go to", ["Dashboard", "Account Settings"])
#             if st.sidebar.button("Log Out", type="secondary"):
#                 self.handle_logout()
#         return page

#     def render_home_page(self):
#         st.title("🚀 Welcome to SaaSify")
#         st.subheader("The ultimate platform to automate, analyze, and scale your business.")
#         st.write("---")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.markdown("### ⚡ Lightning Fast")
#             st.write("Built with modular Python systems for split-second calculations.")
#         with col2:
#             st.markdown("### 💾 Secure Database")
#             st.write("Your profiles are securely hashed and stored locally via production SQLite.")

#     def render_auth_page(self):
#         st.title("🔐 Access Your Account")
        
#         # --- SOCIAL LOGINS SECTION (OIDC) ---
#         st.markdown("### Sign in using Third-Party Providers")
#         col_g, col_l = st.columns(2)
#         with col_g:
#             if st.button("🌐 Connect with Google", use_container_width=True):
#                 st.login("google") # Calls config block [auth.google]
#         with col_l:
#             if st.button("💼 Connect with LinkedIn", use_container_width=True):
#                 st.login("linkedin") # Calls config block [auth.linkedin]
                
#         st.write("---")
#         st.markdown("### Or use your platform account")
        
#         tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
#         with tab1:
#             login_user = st.text_input("Username", key="login_user")
#             login_pass = st.text_input("Password", type="password", key="login_pass")
            
#             if st.button("Log In", type="primary"):
#                 if self.db.verify_user(login_user, login_pass):
#                     st.session_state.logged_in = True
#                     st.session_state.username = login_user
#                     st.success(f"Welcome back, {login_user}!")
#                     time.sleep(0.5)
#                     st.rerun()
#                 else:
#                     st.error("Invalid credentials. Please try again.")
                    
#         with tab2:
#             new_user = st.text_input("Choose a Username", key="new_user")
#             new_email = st.text_input("Email Address", key="new_email")
#             new_pass = st.text_input("Password", type="password", key="new_pass")
#             confirm_pass = st.text_input("Confirm Password", type="password", key="confirm_pass")
            
#             if st.button("Register Account"):
#                 if new_pass != confirm_pass:
#                     st.error("Passwords do not match!")
#                 elif not (new_user and new_email and new_pass):
#                     st.error("Please fill out all fields.")
#                 else:
#                     success = self.db.create_user(new_user, new_email, new_pass)
#                     if success:
#                         st.success("Registration successful! Switch to the 'Sign In' tab.")
#                     else:
#                         st.error("Username or email already taken.")

#     def render_dashboard_page(self):
#         st.title(f"📊 Dashboard: Welcome, {st.session_state.username}!")
        
#         m1, m2, m3 = st.columns(3)
#         m1.metric("Active Users", "1,245", "+12%")
#         m2.metric("Monthly Revenue", "$14,230", "+8%")
#         m3.metric("Server Uptime", "99.98%", "-0.02%")
        
#         st.write("---")
#         chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
#         st.line_chart(chart_data)

#     def render_settings_page(self):
#         st.title("⚙️ Account Settings")
#         st.write(f"Logged in identity: **{st.session_state.username}**")
#         st.checkbox("Enable Notifications", value=True)

#     def run(self):
#         selected_page = self.render_sidebar()
        
#         if selected_page == "Home":
#             self.render_home_page()
#         elif selected_page == "Sign In / Sign Up":
#             if st.session_state.logged_in:
#                 self.render_dashboard_page()
#             else:
#                 self.render_auth_page()
#         elif selected_page == "Dashboard":
#             self.render_dashboard_page()
#         elif selected_page == "Account Settings":
#             self.render_settings_page()

# if __name__ == "__main__":
#     app = SaaSApplication()
#     app.run()
    