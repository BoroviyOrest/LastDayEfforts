import React, {Component} from 'react';
import createBrowserHistory from '../../../routers/history';
import {RawImageTab} from '../../../components/client/RawImageTab'
import io from "socket.io-client";
import imageUrl from '../../../photo_2020-05-23_17-28-32.jpg'


export class RawImageTabContainer extends Component {
    constructor(props) {
        super(props);

        this.state = {
            imageList: [
                {
                    id: 1,
                    name: 'Nature image',
                    createdOn: '05.06.2020 18:50',
                    imageUrl: imageUrl,
                },
            ]
        };
    };

    componentDidMount() {
        const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTkyODYzOTU0LCJqdGkiOiJmM2ZhYWE1YjRjYTU0ODlkOGZmNzQzMDU5Yzg3ZGFkZCIsInVzZXJfaWQiOjF9.IWDf-L8zKjCcxUMwcZ-UTcQFynWAR2VqGEaW6TGa8P0';
        const socket = io.connect(
            'http://127.0.0.1:7000',
            {
                transports: ['websocket'],
                reconnection: false,
                query: {
                    token: token
                }
            }
        );

        socket.on('connect', function () {
            socket.emit('get_image', {image_id: 1}, (data) => {
                console.log(data);
            });
            socket.emit('get_image', {image_id: 2}, (data) => {
                console.log(data);
            });
            socket.emit('get_image', {image_id: 3}, (data) => {
                console.log(data);
            });
        });

        socket.on('message', (data) => {
            console.log(data)
        });

        socket.on('error', (data) => {
            console.log(data.info)
        });

        socket.on('disconnect', (reason) => {
            console.log('server disconnect');
            if (reason !== 'io server disconnect') {
                socket.connect();
            }
        });
    }

    onCardClick = (id) => {
        createBrowserHistory.push(`/raw_image/${id}`);
    };

    render() {
        const {imageList} = this.state;

        return (
            <RawImageTab imageList={imageList} onCardClick={this.onCardClick}/>
        )
    }
};
