/* eslint-disable react/prop-types */
import { Link, useMatch, useResolvedPath } from "react-router-dom"

export default function Navbar() {
	return (
		<nav className="nav">
			<Link to="/" className="site-title">Temp Item</Link>
			<ul>
				<CustomLink to="/game_info">All games</CustomLink>
				<CustomLink to="/game_info/publishers">All publishers</CustomLink>
			</ul>
		</nav>
	)
}


function CustomLink({ to, children, ...props }) {
	const path = useResolvedPath(to)
	const isActive = useMatch({ path: path.pathname, end: true })

	return (
		<li className={isActive ? "active" : ""}>
			<Link to={to} {...props}>{children}</Link>
		</li>
	)
}