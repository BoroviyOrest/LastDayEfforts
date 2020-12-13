import React from 'react';
import {PrivateLayout} from '../../PrivateLayout'
import {StylesAdminTab} from '../../../components/admin/StylesAdminTab'
import {UsersAdminTab} from '../../../components/admin/UserAdminTab'
import {Tabs} from 'antd';

const {TabPane} = Tabs;

export const AdminPage = ({stylesList, styleStats, usersStats, usersList}) => {
    return (
        <PrivateLayout>
            <div>
                <Tabs tabPosition='left'>
                    <TabPane tab="Users stats" key="1">
                        <UsersAdminTab usersList={usersList} usersStats={usersStats}/>
                    </TabPane>
                    <TabPane tab="Styles stats" key="2">
                        <StylesAdminTab stylesList={stylesList} styleStats={styleStats}/>
                    </TabPane>
                </Tabs>
            </div>
        </PrivateLayout>
    );
};
