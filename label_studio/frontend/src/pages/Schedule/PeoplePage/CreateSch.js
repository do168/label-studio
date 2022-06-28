import React from 'react';
import { useHistory } from 'react-router';
import { Button, ToggleItems } from '../../../components';
import { Modal } from '../../../components/Modal/Modal';
import { Space } from '../../../components/Space/Space';
import { useAPI } from '../../../providers/ApiProvider';
import { cn } from '../../../utils/bem';
import { PeopleList } from '../PeoplePage/PeopleList';
import { useParams as useRouterParams } from 'react-router';
import { Redirect } from 'react-router-dom';
import "./CreateProject.styl";

const getCurrentPage = () => {
  const pageNumberFromURL = new URLSearchParams(location.search).get("page");

  return pageNumberFromURL ? parseInt(pageNumberFromURL) : 1;
};


const SchName = ({ name, setName, onSubmit, error, setPeriod, handleSelectProject, handleSelectModel, setTime,
   projectsList, modelsList, tmpChecked, autoChecked, show = true }) => !show ? null :(
  <form className={cn("project-name")} onSubmit={e => { e.preventDefault(); onSubmit(); }}>
    <div className="field field--wide">
      <label htmlFor="sch_name">Sch Name</label>
      <input name="name" id="sch_name" value={name} onChange={e => setName(e.target.value)} />
      {error && <span className="error">{error}</span>}
    </div>
    <div className="field field--wide">
      <label htmlFor="sch_dataset">Dataset</label>
      <select
        id="project_dataset"
        name="dataset"
        onChange={e => handleSelectProject(e)}>
        <option value="" selected disabled hidden >선택하세요.</option>
        {
          projectsList.map((item) => (
            <option value={[item.id, item.title]} key={item.id}>
              {item.title}
            </option>
          ))
        }
      </select>
    </div>
    <div className="field field--wide">
      <label htmlFor="sch_inference_model">Inference Model</label>
      <select
        id="project_model"
        name="model"
        onChange={e => handleSelectModel(e)}>
        <option value="" selected disabled hidden >선택하세요.</option>
        {
          modelsList.map((item) => (
            <option value={[item.id, item.title]} key={item.id}>
              {item.title}
            </option>
          ))
        }
      </select>
    </div>
    <div className="field field--wide">
      <label htmlFor="sch_period">Period</label>
      <div style={{ display: "flex" }}>
        <input
          name="period"
          id="sch_period"
          placeholder="period of your sch"
          rows="1"
          onChange={e=> setPeriod(e.target.value)}
        />
        <select 
          id="project_model"
          name="model"
          style={{width:"30%", height:"33px"}}
          onChange={e=>setTime(e.target.value)}>
            <option value="" selected disabled hidden >선택하세요.</option>
            <option value="1">시간
            </option>
            <option value="168">주
            </option>
            <option value="720">월
            </option>
        </select>

      </div>
    </div>
    <fieldset>
      <legend>
        Group Box
      </legend>
      임시폴더 자동삭제 <input type="checkbox" checked={tmpChecked} ></input>수행 후 Target dataset이 지워집니다(data포함)<br></br>
      프로젝트 자동생성 <input type="checkbox" checked={autoChecked} ></input>수행 후 Label Studio에 자동으로 결과물이 프로젝트에 등록됩니다
    </fieldset>
  </form>
);

export const CreateSch = ({ onClose }) => {
  const [step, setStep] = React.useState("name"); // name | import | config
  const [waiting, setWaitingStatus] = React.useState(false);

  const history = useHistory();
  const api = useAPI();

  const [name, setName] = React.useState("");
  const [error, setError] = React.useState();

  const [dataset, setDataset] = React.useState("");
  const [model, setModel] = React.useState("");
  const [modelId, setModelId] = React.useState("");
  const [period, setPeriod] = React.useState("");
  const [Selected, setSelected] = React.useState("");
  const [projectId, setProjectId] = React.useState("");
  const [sch_time, setTime] = React.useState(1);

  const [projectsList, setProjectsList] = React.useState([]);
  const [modelsList, setModelsList] = React.useState([]);
  const [currentPage, setCurrentPage] = React.useState(getCurrentPage());
  const [totalItems, setTotalItems] = React.useState("");

  const [tmpChecked, setTmpChecked] = React.useState(false);
  const [autoChecked, setAutoChecked] = React.useState(false);

  const defaultPageSize = parseInt(localStorage.getItem('pages:projects-list') ?? 30);

  React.useEffect(() => { setError(null); }, [name]);

  const rootClass = cn("create-sch");
  const tabClass = rootClass.elem("tab");
  const steps = {
    name: <span className={tabClass.mod({ disabled: !!error })}>Sch Name</span>,
  };

  // name intentionally skipped from deps:
  // this should trigger only once when we got project loaded

  const schBody = React.useMemo(() => ({
    title: name,
    dataset:dataset,
    inf_model: model,
    period: period,
    project: projectId,
    model: modelId,
  }), [name, dataset, model, period, projectId, modelId]);

  const onRun = React.useCallback(async () => {
    setWaitingStatus(true);
    const response = await api.callApi('schMlInteractive', {
      params: { pk: modelId, projectId: projectId},
      body: {
        projectId: projectId
      }
    })

    setWaitingStatus(false);
    console.log(response);
    if (response !== null) {
      history.push(`/projects/${projectId}/data`);
    }
  });

  const onCreate = React.useCallback(async () => {
    setWaitingStatus(true);
    console.log("period: ", period);
    console.log("time :", sch_time);
    const calcPeriod = period*sch_time;
    console.log(name, dataset, model, period);
    const response = await api.callApi('createSch',{
      body: {
        title: name,
        dataset: dataset,
        inf_model: model,
        period: calcPeriod,
        tmp_auto_remove: tmpChecked,
        prj_auto_create: autoChecked,
        project: projectId,
        model: modelId,
      },
    });

    setWaitingStatus(false);
    console.log(response)
    if (response !== null) {
      onClose?.();
      location.reload();
    }
  }, [schBody]);

  const fetchProjects = async (page  = currentPage, pageSize = defaultPageSize) => {
    const data = await api.callApi("projects", {
      params: { page, page_size: pageSize },
    });

    setTotalItems(data?.count ?? 1);
    setProjectsList(data.results ?? []);
  };

  const fetchModels = async() => {
    const data = await api.callApi("mLBackendsList", {
    })
    console.log(data);

    setModelsList(data ?? []);
  };

  React.useEffect(() => {
    fetchProjects();
    fetchModels();
  }, []);

  const loadNextPage = async (page, pageSize) => {
    setCurrentPage(page);
    await fetchProjects(page, pageSize);
  };

  const handleSelectProject = async (e) => {
    const [tmpId, tmpProjectTitle] = e.target.value.split(",");
    setProjectId(tmpId);
    setDataset(tmpProjectTitle);
  }

  const handleSelectModel = (e) => {
    console.log(e.target.value);
    const [tmpId, tmpModelTitle] = e.target.value.split(",");
    console.log(tmpId, tmpModelTitle);
    setModelId(tmpId);
    setModel(tmpModelTitle);
  }

  const tempCheckHandler = async () => {
    setTmpChecked(!tmpChecked);
  }

  const autoCheckHandler = async () => {
    setAutoChecked(!autoChecked);
  }

  return (
    <Modal fullscreen visible bare closeOnClickOutside={false}>
      <div className={rootClass}>
        <Modal.Header>
          <h1>Create Sch</h1>

          <Space>
            <Button look="danger" size="compact" onClick={onRun} waiting={waiting}>Run</Button>
            <Button look="primary" size="compact" onClick={onCreate} waiting={waiting} disabled={error}>Save</Button>
          </Space>
        </Modal.Header>
        <SchName
          name={name}
          setName={setName}
          error={error}
          onSubmit={onCreate}
          dataset={dataset}
          setDataset={setDataset}
          model={model}
          setModel={setModel}
          setPeriod={setPeriod}
          tmpChecked={tmpChecked}
          autoChecked={autoChecked}
          handleSelectProject={handleSelectProject}
          handleSelectModel={handleSelectModel}
          setTime={setTime}
          tempCheckHandler={tempCheckHandler}
          autoCheckHandler={autoCheckHandler}
          projectsList={projectsList}
          modelsList={modelsList}
          show={step === "name"}
        />
      </div>
    </Modal>
  );
};
