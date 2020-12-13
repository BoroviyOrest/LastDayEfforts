import React from 'react';
import {Layout} from 'antd';


export const PublicLayout = ({children}) => {
    const {Content} = Layout;

    return (
        <Layout>
            <Content style={{padding: '50px'}}>
                <Layout style={{padding: '50px 0', background: '#fff'}}>
                    {children}
                </Layout>
            </Content>
        </Layout>
    )
};
