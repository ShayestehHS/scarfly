
import axios from 'axios'

export async function Service(method, input) {
    let data = await axios.post('https://api.scarfly.ir/accounts/register/', JSON.stringify({ "phone_number": input.toString() }), { headers: { 'content-type': 'application/json' } })

    return data
}

export async function Retrieve(input) {

    await axios.get(`https://api.scarfly.ir/orders/${input}/`,
        { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access') } }).then(res => {
        }).catch(err => {
            Refresh().then(Retrieve(input))
        })

}


export async function Refresh() {
    if (localStorage.getItem('refresh')) {
        let response = await axios.post(`https://api.scarfly.ir/accounts/refresh/`,
            JSON.stringify({ "refresh": localStorage.getItem('refresh') }),
            { headers: { 'content-type': 'application/json' } })



        setTokens(response.data.access)
        return
    }

}

export async function login(input) {
    let response = await axios.post('https://api.scarfly.ir/accounts/login/', JSON.stringify({ "phone_number": input.toString() }), { headers: { 'content-type': 'application/json' } })
    setTokens(response.data.access, response.data.refresh)
    if (response.status === 200) {
        return response
    }
}

export const register = async (input) => {
    let response = await axios.post('https://api.scarfly.ir/accounts/login/', JSON.stringify({ "phone_number": input.toString() }), { headers: { 'content-type': 'application/json' } })
    setTokens(response.data.access, response.data.refresh)
    if (response.status === 200) {
        return response
    }
}


const setTokens = (access, refresh) => {
    access && localStorage.setItem('access', access)
    refresh && localStorage.setItem('refresh', refresh)
}


export const verify = async () => {
    await Refresh()
    if (localStorage.getItem('access')) {
        const response = await axios.get('https://api.scarfly.ir/accounts/verify/', { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access') } })
        return response
    }


}

export const createOrder = async (input) => {
    const response = await axios.post('https://api.scarfly.ir/orders/create/', input, { headers: { 'Authorization': 'Bearer ' + localStorage.getItem('access') } })
    return response
}


