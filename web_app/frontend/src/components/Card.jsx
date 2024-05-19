/* eslint-disable react/prop-types */
import { Link } from 'react-router-dom'
import '../styles/index.css'

import apple from '../styles/icons/apple.svg';
import xbox from '../styles/icons/xbox.svg';
import playstation from '../styles/icons/playstation.svg';
import chrome from '../styles/icons/chrome.svg';
import android from '../styles/icons/android.svg';
import linux from '../styles/icons/linux.svg';
import desktop from '../styles/icons/desktop-solid.svg';
import game_console from '../styles/icons/game-console-svgrepo-com.svg';
import nintendo_logo from '../styles/icons/nintendo.svg';
import nintendo_switch from '../styles/icons/nintendo-switch.svg';
import sega from '../styles/icons/sega.svg';
import windows from '../styles/icons/windows.svg';

export default function Card ({...props}) {
	const game = props.item

	const icons = {
		"Android": android,
    "Classic Macintosh": desktop,
    "Dreamcast": game_console,
    "Game Boy Advance": game_console,
    "GameCube": game_console,
    "Linux": linux,
    "Nintendo 3DS": nintendo_logo,
    "Nintendo 64": nintendo_logo,
    "Nintendo DS": nintendo_logo,
    "Nintendo Switch": nintendo_switch,
    "PC": windows,
    "PS Vita": playstation,
    "PSP": game_console,
    "PlayStation": playstation,
    "PlayStation 2": playstation,
    "PlayStation 3": playstation,
    "PlayStation 4": playstation,
    "PlayStation 5": playstation,
    "SEGA Saturn": sega,
    "Web": chrome,
    "Wii": nintendo_logo,
    "Wii U": nintendo_logo,
    "Xbox": xbox,
    "Xbox 360": xbox,
    "Xbox One": xbox,
    "Xbox Series S/X": xbox,
    "iOS": apple,
    "macOS": apple
	}

	// Формирование уникальных платформ для игры
	const uniqueIconsSet = new Set()
	game.platforms.map((item) => {
		uniqueIconsSet.add(icons[item])
	})
	const uniqueIcons = [...uniqueIconsSet]
	
	return (
		<Link to={'/game_info/' + game.slug}>
			<div className='card'>
				<img className='w-full top-0 max-h-96' src={game.preview_url} alt={game.name} width={400} />
				<div className='card-info'>

					<div className='flex justify-between items-center'>
						<div className='platforms'>
							{uniqueIcons.map((item, i) => {
								if (item === nintendo_switch || item === nintendo_logo) {
									return (
										<img src={item} key={i} width={30} className='icon'/>
									) 
								} else {
									return (
										<img src={item} key={i} width={17} className='icon'/>
									) 
								}
							})}
						</div>
						<span 
							className={game.score 
								? `score ${game.score >= 75 
									? 'text-green-600 border-green-600' 
									: 'border-yellow-600 text-yellow-600'}` 
								: ''}
						>
							{game.score ? game.score : ''}
						</span>
					</div>

					<div className='font-bold text-xl mb-2 pt-1.5'>{game.name}</div>
				</div>
				<div className='text'>
					<div className='genres'>
						<span>Genres: </span> 
						<span>{game.genres.join(', ')}</span>
					</div>

					<div className='release'>
						<span>Release: </span>
						<span>{game.date.month} {game.date.day}, {game.date.year}</span>
					</div>
				</div>
			</div>
		</Link>
	)
}

