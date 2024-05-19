import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import axios from "axios"
import { Spin, Carousel } from 'antd';
import slugify from 'react-slugify'
import { Link } from "react-router-dom"
import '../styles/single_game.css';
import no_image from '../styles/images/no_image.webp';
import React from "react";

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
	}, [slug])

	return (
		<>
			{game 
				? <>
						<div className="wrapper">

							<div className="text-wrapper">
								<div className="first">
									<h1 className="title">{game.name}</h1>
									<p className="playtime">{game.playtime ? <span>Playtime: {game.playtime}</span> : ''}</p>
								</div>
								<p className="description">{game.description}</p>
							</div>

							<div className="image-wrapper">
								<img src={game.preview_url ? game.preview_url : no_image} width={500}/>
							</div>

						</div>

						<div className="info-wrapper">
							<div className="full-info-wrapper">
								<div className="full-info">
									{game.genres
										? <div className="item">
												<div className="content">
													<p className="info-title">Genres</p>
													<p>{game.genres.join(', ')}</p>
												</div>
											</div>
										: <></>
									}
									{game.score
										? <div className="item">
												<div className="content">
													<p className="info-title">Rating</p>
													<p>{game.score} / 100</p>
												</div>
											</div>
										: <></>
									}
									{game.age
										? <div className="item">
												<div className="content">
													<p className="info-title">Age rating</p>
													<p>{game.age}</p>
												</div>
											</div>
										: <></>
									}
									{game.date
										? <div className="item">
												<div className="content">
													<p className="info-title">Release date</p>
													<p>{game.date.day} {game.date.month} {game.date.year}</p>
												</div>
											</div>
										: <></>
									}
									{game.platforms
										? <div className="item">
												<div className="content">
													<p className="info-title">Platforms</p>
													<p>{game.platforms.join(', ')}</p>
												</div>
											</div>
										: <></>
									}
									{Object.keys(game.publishers).length !== 0
										? <div className="item">
												<div className="content">
													<p className="info-title">Publishers</p>
													<p>
														{Object.keys(game.publishers).map((item, i) => (
															<React.Fragment key={i}>
																<Link className="publisher-link" to={'/game_info/publishers/' + slugify(game.publishers[item]['name'])}>{game.publishers[item]['name']}</Link>
																{i !== game.publishers.length - 1 && <span className="separator"> | </span>}
															</React.Fragment>
														))}
													</p>
												</div>
											</div>
										: <></>
									}
								</div>
							</div>
							<div className="carousel-wrapper">
								<Carousel autoplay={true} infinite={true} className="carousel" autoplaySpeed={2000}>
									{game.photos.map((photo, i) => {
										return (
											<div key={i}>
												<img src={photo} width={500} />
											</div>
										)
									})}
								</Carousel>
							</div>
						</div>
					</> 
				: <div>
						<Spin size="large" />
					</div>
			}
		</>
	)
}