import dash_bootstrap_components as dbc 

navbar_layout = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("🏥 Hospital Readmission Dashboard", href="/", className="ms-2"),

            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href="/")),
                    dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
                    dbc.NavItem(dbc.NavLink("Prediction", href="/prediction")),
                    dbc.NavItem(dbc.NavLink("About", href="/about")),
                ],
                className="ms-auto",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)