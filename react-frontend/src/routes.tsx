/*!

=========================================================
* Argon Dashboard React - v1.2.4
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2024 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Icons from "views/Icons";
import Resume from "views/Resume";
import Jobs from "views/Jobs";

var routes = [
  {
    path: "/resume",
    name: "Resume",
    icon: "ni ni-books text-info",
    component: <Resume />,
    layout: "/admin",
  },
  {
    path: "/jobs",
    name: "Jobs",
    icon: "ni ni-bullet-list-67 text-info",
    component: <Jobs />,
    layout: "/admin",
  },
  {
    path: "/search-job",
    name: "Search Job",
    icon: "ni ni-world-2 text-info",
    component: <Icons />,
    layout: "/admin",
  },
];
export default routes;
