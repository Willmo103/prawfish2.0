// script will dynamically render the links on the nav bar depending on the url the user is on
// home, login, register, only renders the login and register links
// dashboard renders my searches, search, and saved, and logout

window.addEventListener("load", () => {
  const path = window.location.pathname;
  const search = document.getElementById("search_link");
  const mySearches = document.getElementById("mysearches_link");
  const saved = document.getElementById("saved_link");
  const logout = document.getElementById("logout_link");
  const login = document.getElementById("login_link");
  const register = document.getElementById("register_link");

  const logout_html = `<a class="btn btn-outline-success my-2 my-sm-0" href="/logout"
          ><i class="fas fa-sign-out-alt"></i> Logout</a
        >`;

  const login_html = `<a class="btn btn-outline-success my-2 my-sm-0" href="/login"
          ><i class="fas fa-sign-in-alt"></i> Login</a
        >`;

  const register_html = `<a class="btn btn-outline-success my-2 my-sm-0" href="/register"
          ><i class="fas fa-user-plus"></i> Register</a
        >`;

  if (path === "/home" || path === "/login" || path === "/register") {
    search.style.display = "none";
    mySearches.style.display = "none";
    saved.style.display = "none";
    login.innerHTML = login_html;
    register.innerHTML = register_html;
  } else if (path === "/dashboard") {
    login.innerHTML = "";
    register.innerHTML = "";
    register.innerHTML = "";
  } else if (path === "/api_key") {
    search.style.display = "none";
    mySearches.style.display = "none";
    saved.style.display = "none";
    login.innerHTML = "";
    register.innerHTML = "";
    register.innerHTML = "";
  }
});
