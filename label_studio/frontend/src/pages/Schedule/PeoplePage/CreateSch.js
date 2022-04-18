import React from 'react';
import { useHistory } from 'react-router';
import { Button, ToggleItems } from '../../../components';
import { Modal } from '../../../components/Modal/Modal';
import { Space } from '../../../components/Space/Space';
import { useAPI } from '../../../providers/ApiProvider';
import { cn } from '../../../utils/bem';
import "./CreateProject.styl";


const SchName = ({ name, setName, onSaveName, onSubmit, error, dataset, setDataset, model, setModel, period, setPeriod, show = true }) => !show ? null :(
  <form className={cn("sch-name")} onSubmit={e => { e.preventDefault(); onSubmit(); }}>
    <div className="field field--wide">
      <label htmlFor="sch_name">Sch Name</label>
      <input name="name" id="sch_name" value={name} onChange={e => setName(e.target.value)} onBlur={onSaveName} />
      {error && <span className="error">{error}</span>}
    </div>
    <div className="field field--wide">
      <label htmlFor="project_dataset">Dataset</label>
      <textarea
        name="dataset"
        id="project_dataset"
        placeholder="dataset of your sch"
        rows="1"
        value={dataset}
        onChange={e => setDataset(e.target.value)}
      />
    </div>
    <div className="field field--wide">
      <label htmlFor="sch_inference_model">Inference Model</label>
      <textarea
        name="inf-model"
        id="project_inference_model"
        placeholder="inference model of your sch"
        rows="1"
        value={model}
        onChange={e => setModel(e.target.value)}
      />
    </div>
    <div className="field field--wide">
      <label htmlFor="sch_period">Period</label>
      <textarea
        name="period"
        id="sch_period"
        placeholder="period of your sch"
        rows="1"
        value={period}
        onChange={e => setPeriod(e.target.value)}
      />
    </div>
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
  const [period, setPeriod] = React.useState("");

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
    dataset,
    model,
    period
  }), [name, dataset, model, period]);

  const onCreate = React.useCallback(async () => {
    setWaitingStatus(true);
    const response = await api.callApi('createSch',{
      body: {
        title: name,
        dataset: dataset,
        model: model,
        period: period,
      },
    });
    setWaitingStatus(false);

    if (response !== null) {
      history.push(`/schs`);
    }
  }, [sch, schBody]);

  return (
    <Modal onHide={onDelete} fullscreen visible bare closeOnClickOutside={false}>
      <div className={rootClass}>
        <Modal.Header>
          <h1>Create Sch</h1>
          <ToggleItems items={steps} active={step} onSelect={setStep} />

          <Space>
            <Button look="primary" size="compact" onClick={onCreate} waiting={waiting || uploading} disabled={error}>Save</Button>
          </Space>
        </Modal.Header>
        <SchName
          name={name}
          setName={setName}
          error={error}
          onSaveName={onSaveName}
          onSubmit={onCreate}
          dataset={dataset}
          setDatset={setDataset}
          model={model}
          setModel={setModel}
          period={period}
          setPeriod={setPeriod}
          show={step === "name"}
        />
      </div>
    </Modal>
  );
};
