// script will dynamically render the links on the nav bar depending on the url the user is on
// home, login, register, only renders the login and register links
// dashboard renders my searches, search, and saved, and logout

window.addEventListener("load", () => {
  const path = window.location.pathname;
  const search = document.getElementById("search_link");
  const mySearches = document.getElementById("my_searches_link");
  const saved = document.getElementById("saved_link");
  const logout = document.getElementById("logout_link");
  const login = document.getElementById("login_link");
  const register = document.getElementById("register_link");

  if (path === "/home" || path === "/login" || path === "/register") {
    search.style.display = "none";
    mySearches.style.display = "none";
    saved.style.display = "none";
    logout.style.display = "none";
  } else if (path === "/dashboard") {
    login.style.display = "none";
    register.style.display = "none";
  } else if (path === "/api_key") {
    search.style.display = "none";
    mySearches.style.display = "none";
    saved.style.display = "none";
    logout.style.display = "none";
    login.style.display = "none";
    register.style.display = "none";
  }
});
