/* eslint-disable react/prop-types */
import { Link } from 'react-router-dom'
import '../index.css'

export default function Card ({...props}) {
	const game = props.item

	return (
		<Link to={'/game_info/' + game.slug}>
			<div className='max-w-sm rounded overflow-hidden shadow-lg m-4'>
				<img className='w-full' src={game.preview_photo} alt='Game'/>
				<div className='px-6 py-4'>
					<div className='font-bold text-xl mb-2'>{game.name}</div>
						<p className='text-gray-700 text-base'>{game.description}</p>
					<div className='px-6 pt-4 pb-2'>
						{game.genres.map(genre => {
							return (<span key={Math.random()} className='inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2'>{genre}</span>)
						})}
					</div>
				</div>
			</div>
			{/* <div>
				<p>{game.name}</p>
				<p>{game.description}</p>
				<p>{game.score}</p>
				<p>{game.genres}</p>
				<p>{game.date.day}</p>
				<p>{game.publishers}</p>
				<p>{game.age}</p>
				<p>{game.playtime}</p>
				<p>{game.platforms}</p>
				<p>{game.preview_photo}</p>
				<p>{game.photos}</p>
			</div> */}
		</Link>
	)
}