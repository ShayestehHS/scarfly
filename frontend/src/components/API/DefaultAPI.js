import axios from 'axios'

const base_url = 'https://scarfly.ir/api';

export async function Service(method, input) {
    return await axios.post(base_url + 'accounts/register/', JSON.stringify({"phone_number": input.toString()}), {headers: {'content-type': 'application/json'}})
}

export async function Retrieve(input) {

    await axios.get(`${base_url}/orders/${input}/`,
        {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}}).then(res => {
    }).catch(err => {
        Refresh().then(Retrieve(input))
    })

}


export async function Refresh() {
    if (localStorage.getItem('refresh')) {
        let response = await axios.post(`${base_url}/accounts/refresh/`,
            JSON.stringify({"refresh": localStorage.getItem('refresh')}),
            {headers: {'content-type': 'application/json'}})


        setTokens(response.data.access)
        return
    }

}

export async function login(input) {
    let response = await axios.post(base_url + '/accounts/login/', JSON.stringify({"phone_number": input.toString()}), {headers: {'content-type': 'application/json'}})
    setTokens(response.data.access, response.data.refresh)
    if (response.status === 200) {
        return response
    }
}

export const register = async (input) => {
    let response = await axios.post(base_url + '/accounts/login/', JSON.stringify({"phone_number": input.toString()}), {headers: {'content-type': 'application/json'}})
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
        return await axios.get(base_url + '/accounts/verify/', {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}})
    }


}

export const createOrder = async (input) => {
    return await axios.post(base_url + '/orders/create/', input, {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}})
}


