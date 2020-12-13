import React, {Component} from 'react';
import {TransformedImageTab} from '../../../components/client/TransformedImageTab'
import _ from 'lodash';
import imageUrl from '../../../photo_2020-05-23_17-28-35.jpg'


export class TransformedImageTabContainer extends Component {
    constructor(props) {
        super(props);

        this.state = {
            imageList: [
                {
                    id: 1,
                    name: 'Transformed Nature image',
                    createdOn: '05.06.2020 18:53',
                    imageUrl: imageUrl,
                },
            ],
            isModalOpen: false,
            modalImage: {},
        };
    };

    openModal = (id) => {
        const {imageList} = this.state;
        const modalImage = _.find(imageList, (image) => image.id === id);
        this.setState({modalImage, isModalOpen: true});
    };

    closeModal = () => {
        this.setState({isModalOpen: false});
    };

    render() {
        const {imageList, isModalOpen, modalImage} = this.state;

        return (
            <TransformedImageTab
                imageList={imageList}
                isModalOpen={isModalOpen}
                modalImage={modalImage}
                openModal={this.openModal}
                closeModal={this.closeModal}
            />
        )
    }
};
