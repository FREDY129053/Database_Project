import { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom"
import ItemsList from '../components/ItemsList';
import { Spin } from 'antd';
import '../styles/single_publisher.css';
import noPhoto from '../styles/images/no_image.webp';

export default function PublisherInfo() {
	const { slug } = useParams()
	const [games, setGames] = useState([])
	const [publisher, setPublisher] = useState(null)

	const getGames = () => {
		axios.get('http://127.0.0.1:8000/game_info/publishers/' + slug + '/all_games').then(resp => {
			setGames(resp.data)
		})
	}

	const getPublisher = () => {
		axios.get('http://127.0.0.1:8000/game_info/publishers/' + slug).then(resp => {
			setPublisher(resp.data)
		})
	}

	useEffect(() => {
		getGames(),
		getPublisher()
	}, [slug])

	return (
		<>
			{publisher 
				? <>
						<div className="wrapper">

						<div className="text-wrapper">
							<h1 className="title">{publisher.name}</h1>
							<p className="description">{publisher.description}</p>
						</div>

						<div className="image-wrapper">
							<img className='photo' src={publisher.photo_url ? publisher.photo_url : noPhoto} width={400}/>
						</div>

						</div>

						<div className="items">
							<ItemsList items={games} />
						</div>
					</>
				: <Spin size='large' />
			}
			
		</>
	)
}