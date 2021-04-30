const puppeteer = require('puppeteer')
const cleanValueRegex = /\[[0-9]+\]/g
const removeParenthesisRegex = /\(.*\)/g
const removeJapaneseCharactersRegex = /[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]|\?/g
const removeInitialName = /^([A-z]|\s|-)*|\(|\)/g
// const removeFeetMeasureRegex = /\(([0-9]+')([0-9]+.?"?)?\)|\(([A-z]|\s)*\)/g
// const cleanValueRegex = /\[[0-9]+\]|\n/g

const formatValueByKey = (key, value) => {
    value = value.replace(cleanValueRegex, '')
    const valueAsArray = value.split(/\n|;/)

    switch (key) {
        case 'affiliation':
            return (
                valueAsArray.length > 1 ?
                valueAsArray
                    .filter(affiliation => affiliation.length !== 0)
                    .map(affiliation => affiliation.replace(removeParenthesisRegex, '').trim()) :
                valueAsArray[0].replace(removeParenthesisRegex, '').trim()
            )
        case 'occupation': {
            return (
                valueAsArray.length > 1 ?
                valueAsArray
                    .filter(occupation => occupation.length !== 0)
                    .map(occupation => occupation.replace(removeParenthesisRegex, '').trim()) :
                valueAsArray[0] 
            )
        }
        case 'residence':
            return (
                valueAsArray.length > 1 ?
                valueAsArray
                    .filter(residence => residence.length !== 0)
                    .map(residence => residence.replace(removeParenthesisRegex, '').trim()) :
                valueAsArray[0].replace(removeParenthesisRegex, '').trim()
            )
        case 'alias': {
            return valueAsArray.filter(value => value.length !== 0).map(value => {
                const valuesBetweenParenthesis = value.replace(removeInitialName, '').split(',')
                const alias = value.replace(removeParenthesisRegex, '').trim()
                const romaji = valuesBetweenParenthesis[0].replace(removeJapaneseCharactersRegex, '').trim()

                return `${alias} (${romaji})`
            })
        }
        case 'age': {
            const ages = valueAsArray.filter(value => value.length !== 0)
            const lastAge = ages[ages.length - 1]

            return lastAge.replace(removeParenthesisRegex, '').trim()
        }
        case 'height': {
            const heights = valueAsArray.filter(value => value.length !== 0)
            const lastHeight = heights[heights.length - 1]

            return lastHeight.replace(removeParenthesisRegex, '').trim()
        }
        case 'jva':
            return (
                valueAsArray.length > 1 ?
                valueAsArray.filter(jva => jva.length !== 0) :
                valueAsArray[0] 
            )
        case 'bounty': {
            const bounties = valueAsArray.filter(value => value.length !== 0)
            const lastBounty = bounties[0]

            return lastBounty.replace(removeParenthesisRegex, '').trim()
        }
        case 'ename':
            return (
                valueAsArray.length > 1 ?
                valueAsArray.filter(ename => ename.length !== 0) :
                valueAsArray[0] 
            )
        case 'Funi eva':
            return (
                valueAsArray.length > 1 ?
                valueAsArray.filter(funiEva => funiEva.length !== 0) :
                valueAsArray[0] 
            )
        case 'Odex eva':
            return (
                valueAsArray.length > 1 ?
                valueAsArray.filter(odexEva => odexEva.length !== 0) :
                valueAsArray[0] 
            )
        case '4kids eva':
            return (
                valueAsArray.length > 1 ?
                valueAsArray.filter(kidsEva => kidsEva.length !== 0) :
                valueAsArray[0] 
            )
        default: return value
    }
}

const run = async () => {
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await page.goto('https://onepiece.fandom.com/wiki/Sanji')

    const keyValuePairs = await page.$$eval('.pi-item.pi-data.pi-item-spacing.pi-border-color', (options) =>
        options.map((option) => {
            const key = option.getAttribute('data-source')
            const value = option.children[1].innerText

            return {
                key,
                value
            }
        })
    );

    const characterData = {}
    for (const keyValuePair of keyValuePairs)
        characterData[keyValuePair.key] = formatValueByKey(keyValuePair.key, keyValuePair.value)

    console.log(characterData)
    await browser.close()
}

run()