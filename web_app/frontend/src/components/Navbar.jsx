/* eslint-disable react/prop-types */
import { Link, useMatch, useResolvedPath } from "react-router-dom"
import axios from 'axios';
import { useEffect, useState, useRef } from 'react';
import { AiOutlineSearch } from "react-icons/ai";

export default function Navbar() {
	const [search, setSearch] = useState('')
	const [searchAnswer, setSearchAnswer] = useState([])
	const [isOpen, setIsOpen] = useState(false)
	const divRef = useRef(null);

	const handleClickOutside = (e) => {
    if (divRef.current && !divRef.current.contains(e.target)) {
      setIsOpen(false);
    }
  };

	useEffect(() => {
    const handleBodyClick = (e) => {
      handleClickOutside(e);
    };

    document.body.addEventListener('click', handleBodyClick);

    return () => {
      document.body.removeEventListener('click', handleBodyClick);
    };
  }, []);

	const getInfoByName = (name) => {
		if (name !== null || name !== undefined || name !== '') {
			axios.get(`http://127.0.0.1:8000/game_info/search/${name}`).then(resp => {
				setSearchAnswer(resp.data)
			})
		}
	}

	useEffect(() => {
		if (search) {
			setIsOpen(true)
		} else {
			setIsOpen(false)
		}

		const TimeSleep = setTimeout(() => {
			if (search) {
				getInfoByName(search)
			} else {
				setSearchAnswer([])
			}
		}, 300);

		return () => clearTimeout(TimeSleep)
	}, [search])


	return (
		<nav className="nav">
			<Link to="/" className="site-title" onClick={() => setSearch('')}>Logo Here</Link>

			<div onBlur={handleClickOutside} ref={divRef}>
				<div className="input_search">
					<AiOutlineSearch />
					<input
						type="text"
						autoComplete="off"
						placeholder="Поиск игр по названию"
						onChange={(e) => setSearch(e.target.value)}
						value={search}
						onClick={() => setIsOpen(true)}
					/>
				</div>
				<ul className={`search_list ${isOpen ? 'show' : ''}`} >
					{search !== '' && searchAnswer.length !== 0 && isOpen
						? searchAnswer.map((item, i) => {
							return (
								<li key={i}>
									<Link 
										// target="_blank"
										key={i} 
										to={'/game_info/' + item.slug} 
										onClick={() => setTimeout(() => {setIsOpen(false); setSearch('')}, 50)}
									>
										<img src={item.preview_url} width={70} className="pr-1.5"/>
										{item.name}
									</Link>
								</li>
						)})
						: <li>Empty...</li>
					}
				</ul>
			</div>

			<ul className="links">
				<CustomLink to="/game_info" onClick={() => setSearch('')}>All games</CustomLink>
				<CustomLink to="/game_info/publishers" onClick={() => setSearch('')}>All publishers</CustomLink>
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