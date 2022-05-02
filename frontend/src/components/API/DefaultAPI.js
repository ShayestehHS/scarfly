import axios from 'axios'

const base_url = 'https://scarfly.ir/api';

export async function verifyUser() {
    console.log("Verify User")

    const verifyResponse = await verify();
    if (verifyResponse && verifyResponse.status === 200) return true

    const refreshResponse = await refresh();
    if (refreshResponse && refreshResponse.status === 200) return true

    return false
}

export async function refresh() {
    console.log("Refresh");

    const refreshToken = localStorage.getItem('refresh')
    if (!refreshToken) return false;

    return await axios.post(`${base_url}/accounts/refresh/`,
        JSON.stringify({"refresh": refreshToken}),
        {headers: {'content-type': 'application/json'}})
        .then(res => {
            if (res.status === 200) {
                setTokens(res.data.access, refreshToken);
            } else {
                console.log(res)
            }
            return res
        })
        .catch(err => {
            console.log(err)
            console.log(err.response)
            console.log(err.response.data)
            return err.response
        })
}

export async function verify() {
    console.log("Verify")

    const accessToken = localStorage.getItem('access');
    if (accessToken != null) {
        return await axios.get(base_url + '/accounts/verify/',
            {headers: {'Authorization': 'Bearer ' + accessToken}})
            .then(res => {
                if (res.status !== 200) {
                    console.log(res)
                    return false
                }
                return res
            })
            .catch(err => {
                if (err.response.status === 401) {
                    return false
                }
                console.log(err)
                console.log(err.response)
                console.log(err.response.data)
                return err.response
            })
    }
    return null
}

export async function Retrieve(input) {
    console.log("Retrieve")

    await axios.get(`${base_url}/orders/${input}/`,
        {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}}).then(res => {
    }).catch(err => {
        refresh().then(Retrieve(input))
    })
}

export async function loginRegister(input) {
    console.log("LoginRegister")

    const loginResponse = await login(input);
    if (loginResponse === true) return true

    const registerResponse = await register(input);
    if (registerResponse === true) return true

    return false
}

export async function login(input) {
    console.log("Login")

    return await axios.post(base_url + '/accounts/login/',
        JSON.stringify({"phone_number": input.toString()}),
        {headers: {'content-type': 'application/json'}})
        .then(response => {
            if (response.status === 200) {
                setTokens(response.data.access, response.data.refresh)
                return true
            }
            return false
        }).catch(err => {
            console.log(err)
            console.log(err.response)
            console.log(err.response.data)
            return false
        })
}

export async function register(input) {
    console.log("Register")

    const response = await axios.post(base_url + '/accounts/register/',
        JSON.stringify({"phone_number": input.toString()}),
        {headers: {'content-type': 'application/json'}}
    ).then(response => {
        if (response.status === 201) {
            setTokens(response.data.access, response.data.refresh)
            return true
        }
        return response
    }).catch(err => {
        console.log(err)
        console.log(err.response)
        console.log(err.response.data)
        return err.response
    })
    console.log(response)
    return response === true
}

export async function retrieveUserData(setName, setFamily) {
    console.log("Retrieve user data")

    let accessToken = localStorage.getItem('access')
    if (accessToken === null) return false

    return await axios.get(base_url + '/accounts/retrieve/',
        {headers: {'Authorization': 'Bearer ' + accessToken}})
        .then(response => {
            if (response.status === 200) {
                setName(response.data.first_name)
                setFamily(response.data.last_name)
                return response.data
            }
            console.log(response)
            console.log(response.data)
            return false
        }).catch(err => {
            console.log(err)
            if (err.response && err.response.status === 401) {
                return false
            }
            console.log(err.response)
            console.log(err.response.data)
        })
}

export const createOrder = async (input) => {
    return await axios.post(base_url + '/orders/create/', input, {headers: {'Authorization': 'Bearer ' + localStorage.getItem('access')}})
        .catch(err => {
            if (err.response.status === 404) return err.response

            console.log(err)
            console.log(err.response)
            console.log(err.response.data)
        })
}

const setTokens = (access, refresh) => {
    access && localStorage.setItem('access', access)
    refresh && localStorage.setItem('refresh', refresh)
}