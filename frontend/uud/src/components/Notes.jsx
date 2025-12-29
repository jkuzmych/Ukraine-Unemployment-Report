import './Notes.css'

const notes = {
    Unemployment_by_category : [
        'Source: https://www.ukrstat.gov.ua/operativ/open_data/menu/rp_vd.htm',
        'Frequency: Quarterly, for 2015-2021 years',
        'Note: 1. Unemployment rate is a quantitative indicator calculated by the ratio of unemployed people to the total labour force. ',
        '      2. Information is based on the results of Labour Force Survey (before 2019 -population (households) sample survey on issues of economic activity).',
        '      3. Data exclude the temporarily occupied territory of the Autonomous Republic of Crimea, the city of Sevastopol and a part of temporarily occupied territories in the Donetsk and Luhansk regions.',
        '      4. Unemployed (by ILO) are  persons aged 15 years and over (before 2019‒15-70 years) who did not have a job in the surveyed week, actively sought it for four weeks and are ready to start work within the next two weeks. The category of the unemployed includes also persons who will start working during the next two weeks; have found a job or await a reply, etc.'
    ],
    Unemployment_real_registered : [
        'Source: https://index.minfin.com.ua/ua/labour/unemploy/',
        'Frequency: yearly, the number of "labour force", "unemployed" population, as well as the number of officially registered unemployed are given in the average period (from the beginning of the year by quarter or year).',
        'Notes: The number of unemployed people is calculated according to the ILO (International Labor Organization) methodology. According to this methodology, a person is considered unemployed if, for four weeks, they: were unemployed, were looking for work, or were available for work.'
    ]
}

export const Unemployment_by_category_Notes = () => {
    return(
        <div className='notes-container'>
            <h2>Notes</h2>
            <hr></hr>
            {notes.Unemployment_by_category.map((element, idx) => (
                <p key={idx}>{element}</p>
            ))}
        </div>
    )
}

export const Unemployment_real_registered_Notes = () => {
    return(
        <div className='notes-container'>
            <h2>Notes</h2>
            <hr></hr>
            {notes.Unemployment_real_registered.map((element, idx) => (
                <p key={idx}>{element}</p>
            ))}
        </div>
    )
}

export default Unemployment_by_category_Notes;
