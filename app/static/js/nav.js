// // script will dynamically render the links on the nav bar depending on the url the user is on
// // home, login, register, only renders the login and register links
// // dashboard renders my searches, search, and saved, and logout

// window.addEventListener("load", () => {
//   const path = window.location.pathname;
//   console.log(path);
//   const buttons_div = document.getElementById("buttons_div");
//   const search = document.getElementById("search_link");
//   const mySearches = document.getElementById("mysearches_link");
//   const saved = document.getElementById("saved_link");
//   const logout = document.getElementById("logout_link");
//   const login = document.getElementById("login_link");
//   const register = document.getElementById("register_link");

//   const logout_html = ``;

//   const login_html = ` `;

//   const register_html = `</div>
//         <div class="form-inline my-2 my-lg-0" id="register_link">
//           <a class="btn btn-outline-success my-2 my-sm-0" href="/register"
//             ><i class="fas fa-user-plus"></i> Register</a
//           >
//         </div>`;

//   if (path == "/home" || path == "/login" || path == "/register") {
//     search.style.display = "none";
//     mySearches.style.display = "none";
//     // saved.style.display = "none";
//     buttons_div.innerHTML = login_html + register_html;
//     console.log("Test string: ", buttons_div.innerHTML);
//   } else if (path === "/dashboard") {
//     logout.innerHTML = logout_html;
//     login.innerHTML = logout_html;
//   } else if (path === "/api_key") {
//     search.style.display = "none";
//     mySearches.style.display = "none";
//     // saved.style.display = "none";
//     buttons_div.innerHTML = login_html + register_html;
//   }
// });
