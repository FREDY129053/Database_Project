import Card from "./Card"

/* eslint-disable react/prop-types */
export default function ItemsList({...props}) {
	const allItems = props.items

	return (
		<>
			<div className="grid grid-cols-3 gap-4">
				{allItems.map(item => {
					if (Object.hasOwn(item, 'genres')) {
						return (<Card key={Math.random()} item={item} />)
					} else {
						return (
							<div key={Math.random()} className='max-w-sm rounded overflow-hidden shadow-lg m-4'>
								<img className='w-full' src={item.photo_url} alt='Publisher'/>
								<div className='px-6 py-4'>
									<div className='font-bold text-xl mb-2'>{item.name}</div>
										<p className='text-gray-700 text-base'>{item.description}</p>
								</div>
							</div>
						)
					}
				})}
			</div>
		</>
	)
}