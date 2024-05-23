/* eslint-disable react/prop-types */
import { useEffect, useState } from 'react';
import { Spin } from 'antd';
import axios from 'axios';
import '../styles/index.css';
import '../styles/dropdown.css';
import ItemsList from '../components/ItemsList';
import ReactPaginate from 'react-paginate'
import PrevArrow from '../styles/icons/arrow-prev.svg';
import NextArrow from '../styles/icons/arrow-next.svg';

export default function Home () {
	const [allGames, setAllGames] = useState([])
	const [filters, setFilters] = useState([])

	const [currPage, setCurrPage] = useState(1)
	const handlePageChange = ({ selected }) => {
		setCurrPage(selected + 1)
		window.scrollTo(0, -2000)
	}

	const [genres, setGenres] = useState([])
	const [platforms, setPlatforms] = useState([])
	const [sort, setSort] = useState()
	
	const getAllGames = (page = 1, filters_genre = [], filters_platform = [], sort = null) => {
		let query = `http://127.0.0.1:8000/game_info/?page=${page}`

		if (sort !== null || sort !== undefined) {
			query += `&sort=${sort}&`
		}

		filters_genre.forEach((filter) => { query += `genres=${filter}&` })
		filters_platform.forEach((filter) => { query += `platforms=${filter}&` })

		axios.get(query).then(resp => {
			setAllGames(resp.data)
		})
	}

	const getFilters = () => {
		axios.get('http://127.0.0.1:8000/game_info/filters').then(resp => {
			setFilters(resp.data)
		})
	}

	useEffect(() => {
		getAllGames(currPage, genres, platforms, sort),
		getFilters()
	}, [currPage, genres, platforms, sort])

	useEffect(() => {
		setCurrPage(1)
	}, [genres, platforms, sort])

	return (
		<>
			{allGames.length != 0 && filters.length != 0
			? <div className='pb-1'>
					<div className='flex pb-10'>
						<Dropdown text='Genres' filters={filters.genres} value={genres} onChange={o => setGenres(o)} multiple={true} />
						<Dropdown text='Platforms' filters={filters.platforms} value={platforms} onChange={o => setPlatforms(o)} multiple={true} />
						<Dropdown text='Sort by' filters={['Rating', 'Date']} value={sort} onChange={o => setSort(o)} multiple={false} />
					</div>
					<ItemsList items={allGames.games} />
					<ReactPaginate
						breakLabel=''
						pageCount={allGames.info.total_pages}
						onPageChange={handlePageChange}
						containerClassName='pagination'
						pageRangeDisplayed={4}
						nextLabel={<img src={NextArrow} className={`next-btn ${currPage === allGames.info.total_pages ? 'hidden' : 'active'}`} />}
						previousLabel={<img src={PrevArrow} className={`prev-btn ${currPage === 1 ? 'hidden' : 'active'}`}/>}
					/>
				</div>
			: <Spin size='large' />}
			
		</>
	)
	
}


export function Dropdown({ multiple, value, onChange, filters, text }) {
	const [isOpen, setIsOpen] = useState(false)
	const [highlightedIndex, setHighlightedIndex] = useState(0)

	function clearOptions() {
		multiple ? onChange([]) : onChange(undefined)
	}

	function selectOption(option) {
		if (multiple) {
			if (value.includes(option)){
				onChange(value.filter(o => o !== option))
			} else {
				onChange([...value, option])
			}
		} else {
			if (option !== value) onChange(option)
		}
	}

	function isOptionSelected(option) {
		return multiple ? value.includes(option) : option === value
	}

	useEffect(() => {
		if (isOpen) setHighlightedIndex(0)
	}, [isOpen])

	return (
			<div onBlur={() => setIsOpen(false)} onClick={() => setIsOpen(!isOpen)} tabIndex={0} className='container'>
				{multiple ? (
						<span className='value'>
							{value.length === 0 ? (
								<label>{text}</label>
							) : (
								value.map((v, i) => (
									<button 
										key={i} 
										onClick={e => {
											e.stopPropagation()
											selectOption(v)
										}}
										className='option_badge'
									>
										{v}
										<span className='remove_btn'>&times;</span>
									</button>
								))
							)}
						</span>
					) : (
						<span className='value'>
							{value === undefined ? (
								<label>{text}</label>
							) : (
								value
							)}
						</span>
					)
				}
				<button onClick={e => {
					e.stopPropagation()
					clearOptions()
				}} 
					className='clear_btn'>&times;
				</button>
				<div className='divider'></div>
				<div className='caret'></div>
				<ul className={`options ${isOpen ? 'show' : ''}`}>
					{filters.map((option, i) => (
						<li
							onClick={e => {
								e.stopPropagation()
								selectOption(option)
								setIsOpen(false)
							}}
							onMouseEnter={() => setHighlightedIndex(i)}
							key={i} 
							className={`option ${isOptionSelected(option) ? 'selected' : ''} ${i === highlightedIndex ? 'highlighted' : ''}`}
						>
							{option}
						</li>
					))}
				</ul>
			</div>

	)
}