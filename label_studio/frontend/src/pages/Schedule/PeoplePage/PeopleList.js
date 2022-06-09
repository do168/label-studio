import { formatDistance } from "date-fns";
import React, { useCallback, useEffect, useState } from "react";
import { Pagination, Spinner, Userpic } from "../../../components";
import { usePage, usePageSize } from "../../../components/Pagination/Pagination";
import { useContextProps } from '../../../providers/RoutesProvider';
import { useAPI } from "../../../providers/ApiProvider";
import { Block, Elem } from "../../../utils/bem";
import { isDefined } from "../../../utils/helpers";
import { useUpdateEffect } from "../../../utils/hooks";
import { CreateSch } from "./CreateSch";
import { Button } from "../../../components";
import { absoluteURL } from '../../../utils/helpers';
import { Oneof } from '../../../components/Oneof/Oneof';
import './PeopleList.styl';

const getCurrentPage = () => {
  const pageNumberFromURL = new URLSearchParams(location.search).get("page");

  return pageNumberFromURL ? parseInt(pageNumberFromURL) : 1;
};

export const EmptySchsList = ({ openModal }) => {
  return (
    <Block name="empty-schs-page">
      <Elem name="header" tag="h1">Heidi doesn’t see any schs here</Elem>
      <p>Create one</p>
      <Elem name="action" tag={Button} onClick={openModal} look="primary">Create Schedule</Elem>
    </Block>
  );
};

export const PeopleList = ( { schsList }) => {
  // useEffect(() => {
  //   if (isDefined(defaultSelected) && schsList) {
  //     const selected = schsList.find(({ user }) => user.id === Number(defaultSelected));

  //     if (selected) selectUser(selected.user);
  //   }
  // }, [schsList, defaultSelected]);

  let state = {
    List: schsList,
    MasterChecked: false,
    SelectedListL: [],
  }

  const onMasterCheck = (e) => {
    let tempList = this.state.List;
    // Check/ UnCheck All Items
    tempList.map((schedule) => (schedule.selected = e.target.checked));

    //Update State
    this.setState({
      MasterChecked: e.target.checked,
      List: tempList,
      SelectedList: this.state.List.filter((e) => e.selected),
    });
  };

  return (
    <>
      <Block name="sch-list">
        <Elem name="wrapper">
          <Elem name="schs">
            <Elem name="header">
              <Elem name="column" mix="form-check-input"> 
                <input type="checkbox" className="form-check-input" checked={state.MasterChecked} id="mastercheck" onChange={e=> onMasterCheck(e)}
                />
              </Elem>
              <Elem name="column" mix="title">Name</Elem>
              <Elem name="column" mix="dataset">Dataset</Elem>
              <Elem name="column" mix="model">model</Elem>
              <Elem name="column" mix="period">period</Elem>
              <Elem name="column" mix="tmp-auto-remove">임시폴더 자동삭제</Elem>
              <Elem name="column" mix="prj-auto-create">프로젝트 자동생성</Elem>
              <Elem name="column" mix="last-activity">Last Activity</Elem>
              <Elem name="column" mix="created-by">Created By</Elem>
            </Elem>
            <Elem name="body">
              {schsList.map((sch) => {

                return (
                  <Elem key={`sch-${sch.id}`} name="sch">
                    <Elem name="field" mix="form-check-input">
                      <input type="checkbox" checked={false} className="form-check-input" onChange={e=> onMasterCheck(e)} />
                    </Elem>
                    <Elem name="field" mix="title">
                      {sch.title}
                    </Elem>
                    <Elem name="field" mix="dataset">
                      {sch.dataset}
                    </Elem>
                    <Elem name="field" mix="model">
                      {sch.inf_model}
                    </Elem>
                    <Elem name="field" mix="period">
                      {sch.period}
                    </Elem>
                    <Elem name="field" mix="tmp-auto-remove">
                      {sch.tmp_auto_remove==true ? "true" : "false"} 
                    </Elem>
                    <Elem name="field" mix="prj-auto-create">
                      {sch.prj_auto_create==true ? "true" : "false"}
                    </Elem>
                    <Elem name="field" mix="last-activity">
                      {sch.updated_at}
                    </Elem>
                    <Elem name="field" mix="created-by">
                      {sch.created_by.email}
                    </Elem>
                  </Elem>
                )
              })}
            </Elem>
          </Elem>
        </Elem>
      </Block>
    </>
  );
};
