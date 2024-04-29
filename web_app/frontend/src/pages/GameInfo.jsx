import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import axios from "axios"
import { Spin } from 'antd';

export default function GameInfo() {
	const { slug } = useParams()
	const [game, setGame] = useState(null)

	const getGame = () => {
		axios.get('http://127.0.0.1:8000/game_info/' + slug).then(resp => {
			setGame(resp.data)
		})
	}

	useEffect(() => {
		getGame()
	}, [])

	return (
		<>
			{game ? <><h1>{game.name}</h1><h1>{game.age}</h1></> : <Spin size="large" />}
		</>
	)
}