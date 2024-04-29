import { useEffect, useState } from 'react';
import { Spin } from 'antd';
import axios from 'axios';
import '../index.css';
import ItemsList from '../components/ItemsList';

export default function Home () {
	const [allGames, setAllGames] = useState([])
	const [genres, setGenres] = useState([])

	const getAllGames = () => {
		axios.get('http://127.0.0.1:8000/game_info').then(resp => {
			setAllGames(resp.data)
		})
	}

	const getGenres = () => {
		axios.get('http://127.0.0.1:8000/game_info/genres').then(resp => {
			setGenres(resp.data)
		})
	}

	useEffect(() => {
		getAllGames(),
		getGenres()
	}, [])

	return (
		<>
			{allGames || genres ? <ItemsList items={allGames} /> : <Spin size='large' />}
			{console.log(genres)}
		</>
	)
	
}