import React, {Component} from 'react';
import {RawImagePage} from '../../../components/client/RawImagePage'
import imageUrl from '../../../photo_2020-05-23_17-28-32.jpg'


export class RawImagePageContainer extends Component {
    constructor(props) {
        super(props);

        this.state = {
            image: imageUrl,
            name: 'Nature image',
            description: 'Created on 05.06.2020 18:50',
            stylesList: [
                {
                    id: 1,
                    description: 'Baroque',
                },
                {
                    id: 2,
                    description: 'Renaissance',
                },
                {
                    id: 3,
                    description: 'Modern',
                },
                {
                    id: 4,
                    description: 'Cubism',
                },
                {
                    id: 5,
                    description: 'Graphics',
                },
            ],
        };
    };

    render() {
        const {image, name, description, stylesList} = this.state;

        return (
            <RawImagePage image={image} name={name} stylesList={stylesList} description={description}/>
        )
    }
};
