# Chemometrics Support Tools
Chemometrics Support Tools is a simple system, projected to support the development process of the scientist project pipeline.
<br />
<br />
The project is divided into two sections:
1. [System solutions](#source-code) supporting the development process in dynamically changing project conditions (basic modules, example implementation, encapsulation, self-commenting and clean code),
2. [Example analysis](#analysis-examples), system use-case, observations and workflow related to problems in the field of chemometrics (examples of solving the most common problems, full workflow from loading data to obtaining the first results).

A detailed description is available in the following chapters, you can access them directly by using the links above.
<br />

Default project structure includes the following directories:
- **notebooks** - directory to store analysis files,
- **src**- source code files,
- **data** (optionaly) - directory to store datasets, checkpoints and results. Can be changed in [Paths][1] class or 
  just omitted in case of passing in-code paths defined on your own,
- **images** - intended for images used in jupyter notebooks and readme file.

[1]:../main/src/readers/paths.py

### Roadmap 
- ~~A universal wrapper that unpacks a data package, processes selected data and then returns the data package~~
- ~~Basic file management tool (url, .json, .csv, .pkl)~~
- ~~Add a dynamic tool generation using Jupyter widgets~~
- ~~Support for multiple folds/batches~~
- ~~Support for methods that work with more than one data set~~
- ~~Add protection against overwriting files and path generation~~
- ~~Add parent-mutable configuration objects~~
- **WIP** Add an example analysis - classification
- **WIP** Add an example analysis - regression
- Refactor interactive widget generator to object oriented Jupyter Widgets GUI 
- Add a database and query support from the reader level
- Real-time data processing and results preview (IPC and Flask)
- Add an example of analysis of data from the Calorimeter
- Add an example of analysis of photos with brain disorders/diseases
<br />

## Tools: First look into source code<a id="source-code"></a>
In the early phases of projects the data structures, instrumentation, and processing methods change frequently.
This causes a lot of problems: getting stuck in a constant refactoring process instead of development, 
lack of time to implement TDD solutions, errors detected too late because the data format changed at the last minute...
<br />
<br />
This time my goal is to develop a lightweight system that will provide convenient access to basic tools, while remaining as flexible and resistant as possible.
```bash
src
|-- graphs
|   |-- constants
|   `-- static
|-- processing
|   |-- format
|   |   `-- constants
|   `-- methods
`-- readers
```

The source code structure is divided into branches, one for each module:
- [graphs][2] - a section that stores the source code of frequently used charts to improve the readability of notebooks; also constant classes for generators and interactive modules,
- [processing][3] - a section that collects:
  - the static ***processing methods***,
  - a ***dataset constants***, ***configurations*** and allowed co-occurrence,
  - a ***data handling*** scenarios (batch processing, feeding data to a method, updating a fold/handling the result),
- [readers][4] (optionaly) - a module supporting file and path management.

[2]:../main/src/graphs
[3]:../main/src/processing
[4]:../main/src/readers
<br />

### Processing methods collection - data format wrapers
In order to implement the data handling interface, I decided to use a multi-level wrapper. Thanks to this approach, adding the method to the system, maintaining the code and its subsequent modification is simple. In order to include [new variants of feeding data](#unpacking) to the method and [handling the result](#packing), simply declare a new `DataFormat` wrapper case and include it in the [configuration class](#configuration).
<br />
<br />
To include a method in the library, just add a `@data_interface` wrapper to it along with the default configuration as in the example:
```python
@data_interface(instruction=DataFoldsConstants.example_group.example_config)
def example_method(
        y: np.ndarray = None,
        example_arg: int = 151
) -> np.ndarray:
  # Your method body: cast from external library or writen on your own
```
The wrapper used is argument-wise. The call is made by passing the `data` key with an appropriate argument, and the configuration of the operations used (unpacking, processing and packing instructions) is provided using the `instruction` key. If the `data` key is missing, the method will be executed without the involvement of the wrapper.

Below you can find practical application examples:
- [Example methods source code](../main/src/processing/methods/filter.py)
- [Example configuration source code](../main/src/processing/format/constants/constants_spectroscopy_nmr.py)

<br />

#### Clean cast
To call a method without a wrapper, call it as in the definition:
```python
processed_data = [
  Preprocessor.library.method(y=data_line, example_arg=arg_val) for data_line in data_fold[label].to_list()
]
```

Calling it without the `data` key will have the same effect as if the method were declared without a wrapper:

```python
def example_method(
        y: np.ndarray = None,
        example_arg: int = 151
) -> np.ndarray:
  # Your method body: cast from external library or writen on your own
```
<br />

#### Wrapper cast
To call a wraper we need to pass nested dataset as an argument of key `data`:
```python
processed_fold_data = Preprocessor.library.method(data=nested_dataset, example_arg=arg_val)
```
Takes the same effect as equivalent below:
```python
processed_nested_data = {}
for fold_name, fold_data in nested_data:
    processed_data = [
    Preprocessor.library.method(y=data, example_arg=arg_val) for data in fold_data[label].to_list()
  ]
  fold_data[label] = processed_data
  processed_nested_data.update({fold_name: fold_data})
```
If the `instruction` key is not provided, the method will be called in the configuration set as the default value in the method definition.
<br />

#### Complex cases

For more complex cases, for example:
- when we want to retrieve more than one column from the set and update only one of them (methods f(x) with a given axis or f(x,y), synchronizing data from multiple sources),
- modify several columns at the same time with the same method (data and axes trimming, normalization operations),
- process training data and, based on the obtained result, process test data...

To add desired operations to the library, include them in the provided sections and then call them by setting the default `instructions` key along with the appropriate `PreprocessorConfiguration` object. Details can be found in later chapters.
<br />

#### Parent-mutable configuration objects<a id="configuration"></a>

Instructions and configurations are stored in an object that inherits the `constant class` based on the passed reference. 
The `configuration class` is defined inside the `wrapper`. This structure is compatible with PEP-8 and allows you to avoid many conflicts or recursive loops.

Additionally, this way you can pass on the methods necessary to execute the instructions. All you need to do is include them in the `constant class` declaration and call them at the `wrapper` level, which handles the data packing and unpacking instructions.
Moreover, `data security methods` can also be placed inside a `constant class`.

Thanks to this procedure, you can avoid complicated modifications and keep the code clean. This way, methods will not have to be written as universal, which facilitates development.
To better understand the construction, let's look at the simplified code below:

```python
def PreprocessorConfiguration(
    example_constructor_instruction_arg,
    parent_class: type(PreprocessorConstants) = PreprocessorConstants,
) -> object:

    class PreprocConfig(parent_class):

        _EXAMPLE_STRUCTURE_CONSTANTS: dict = {}
  
        def __init__(self, _example_constructor_instruction_arg):
            super().__init__()
            self.example_constructor_instruction_arg = _example_constructor_instruction_arg

        def example_configuration_class_method(self):
            # Do Something

    return PreprocConfig(example_constructor_instruction_arg)

```

To better understand how the mechanism works, I recommend reviewing 
[configuration class source code](../main/src/processing/format/constants/constants_template.py).
<br />
<br />
To add support for your own data (column names, packing and unpacking instructions), create a child class based on the previously mentioned template:

```python
from src.processing.format.constants.constants_template import *

class ConstantsExample(PreprocessorConstants):

    Y_EXAMPE: str
    X_EXAMPLE: str

    def __init__(self):
        super().__init__()

        self.Y_EXAMPLE = "x_example_label"
        self.X_EXAMPLE = "y_example_label"

        self.DATA_FORMAT_AVAILABLE_Y = [
            self.Y_EXAMPLE
        ]

        self.DATA_FORMAT_AVAILABLE_X = [
            self.X_EXAMPLE
        ]
```

Then create a configuration object, providing appropriate instructions, column names and a reference to the configuration class as arguments:

```python
_CONST: ConstantsExample = ConstantsExample()

ExampleConfigYofX = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_Y_OF_X,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_Y,
    instruction_unpack={"y": _CONST.Y_EXAMPLE, "x": _CONST.X_EXAMPLE},
    instruction_pack={"y": _CONST.Y_EXAMPLE},
    parent_class=ConstantsExample
)
```

The prepared object can be passed as the value of the `instructions` key when calling:

```python
example_method(data=nested_dataset, instruction=ExampleConfigYofX, example_arg=arg_val)
```

Or set it as the default wrapper value when declaring the method:

```python
@data_interface(instruction = ExampleConfigYofX)
```

You can find an example of 
[configuration objects implementation](../main/src/processing/format/constants/constants_calorimetry.py) 
here.
<br />

##### Extracting switch-case<a id="unpacking"></a>

Below you can see an example of the implementation of data handling operations that will be provided to the method. The first argument `data_format` is a switch-case wrapper argument, it is only used to distinguish the methods we want to call.

```python
@data_unpack.format(PreprocessorConstants().PROCESS_DATA_AS_Y_OF_X)
def _unpack_wrapper_data_as_y_of_x(
        data_format: int,
        data: dict,
        instruction: dict,
        **kwargs
) -> list:

    X = data.get(instruction.get("x")).tolist()
    Y = data.get(instruction.get("y")).tolist()

    if WrapperOperations.is_matrix_1d(X):
        return [{**kwargs, **{"y": y}, **{"x": X}} for y in Y]
    else:
        return [{**kwargs, **{"y": y}, **{"x": X[idx]}} for idx, y in enumerate(Y)]
```

[Practical example and default workspace directory](../main/src/processing/format/data_wrapper_format_pack.py)
<br />
<br />
<br />
The batches/folds handling protocol can be found
[here](../main/src/processing/format/data_wrapper_folds.py)
. It is worth remembering that the method will be called using list comprehension.:

```python
result = [function(**data_dict) for data_dict in data_unpacked]
```

So it is recommended to extract data into a structure such that each calculation operation can be called separately, for example:

```python
[
  {"y":data_line_0, **method_kwargs},
    ...
  {"y":data_line_n, **method_kwargs}
]
```

This facilitates subsequent modification of the code to support multiprocessing. 
<br />

##### Updating switch-case<a id="packing"></a>
Below you can see an example of implementing a data update operation. The first argument `data_format` is a switch-case wrapper argument, it is only used to distinguish the methods we want to call.

```python
@data_pack.format(PreprocessorConstants().PROCESS_DATA_AS_Y)
def _pack_wrapper_result_as_y(
        data_format: str,
        data: dict,
        instruction: dict,
        result: list
) -> dict:

    data.update({instruction.get("y"): result})
    return data
```

[Practical example abd default workspace directory](../main/src/processing/format/data_wrapper_format_unpack.py)
<br />

### Dynamic figures and iteractive widgets

**WIP**
<br />

### File management

**WIP**
<br />

## Example analysis - Notebooks Use Cases<a id="analysis-examples"></a>
The main goal I wanted to achieve when creating this notebook was to summarize my observations acquired while working with optical data.
<br />
<br />
Books for beginners usually only cover the basics of statistics; modern algorithms are often omitted or described in a very general and impractical way. This forces the reader to look for solutions in specialized literature, which focuses on a lot of theory and details, instead of showing a practical solution to the problem. The high entry level makes people decide to use ready-made software, often skipping theoretical preparation.
<br />
<br />
During my professional life, I came across a lot of articles where bizarre mistakes were made. Overtrained models, failure to take into account factors co-occurring during the experiment, incorrectly calculated correlation factors, lack of basic optimizations or checking the impact of the method used on the signal quality.
<br />

Mastering these issues requires extensive knowledge, often from several disciplines. The answers are scattered among specialized books in the field of:
- ***electronics*** and ***signal processing techniques*** (properties of the sensors used, effects related to instrumentation, noise properties and co-occurring interferences, technological limits),
- ***programming***, ***algorithms***, and ***archtecture*** used (selection of tools and architecture, CI-CD, TDD implementation),
- ***mathematics*** and ***modern analysis techniques*** (data augmentation, feature-selection, validation, modeling, ML and NN tools),
- as well as knowledge about the object or scientific experiment we are examining.

```bash
notebooks
|-- 00_wine_spectra_analysis_fourier_infrared.ipynb
|-- 00_wine_spectra_baseline_calibration_interactive_example.ipynb
|-- 01_coffees_spectra_analysis_nuclear_magnetic_resonance.ipynb
`-- interactive_diagrams.ipynb
```
Description of the file contents with links to selected sections:
- [00_wine_spectra_analysis_fourier_infrared.ipynb ](#analysis-examples-ftir) - a classification-based approach - FTIR spectra analysis of Cabernet and Shiraz wines,
- [00_wine_spectra_baseline_calibration_interactive_example.ipynb ](#analysis-examples-interact) - example of manual calibration of the selected method - widget generation and real-time processing,
- [01_coffees_spectra_analysis_nuclear_magnetic_resonance.ipynb ](#analysis-examples-nmr) - a regression-based problem solution - 16-O-Methylcafestol concentration in coffee NMR spectra,
- [interactive_diagrams.ipynb ](#analysis-examples-interact-sc) - notebook source file.
<br />

### Spectral analysis - Classification **WIP**<a id="analysis-examples-ftir"></a>
[**Wine spectra with Fourier-Transform Infra Red spectrometer**](../main/notebooks/00_wine_spectra_analysis_fourier_infrared.ipynb)
<br />
**WIP**
<br />
<br /> [Dataset](https://github.com/QIBChemometrics/Wine_Cabernet_Shiraz_FTIR#wine_cabernet_shiraz_ftir)
<br /> [Reference material](https://www.sciencedirect.com/science/article/abs/pii/S0956713519302294?via%3Dihub)
<br />

### Spectral analysis - Regression **WIP**<a id="analysis-examples-nmr"></a>
[**Coffee as Nuclear Magnetic Resonance spectrum**](../main/notebooks/01_coffees_spectra_analysis_nuclear_magnetic_resonance.ipynb)
<br />
**WIP**
<br />
<br /> [Dataset](https://github.com/QIBChemometrics/Benchtop-NMR-Coffee-Survey)
<br /> [Supplementary data](https://ars.els-cdn.com/content/image/1-s2.0-S0308814617319829-mmc1.pdf)
<br /> [Reference material](https://www.sciencedirect.com/science/article/pii/S0308814617319829?via%3Dihub)
<br />

### Real-time Interactive Widgets Example<a id="analysis-examples-interact"></a>
[**Manual calibration of methods in live-processed-diagrams**](../main/notebooks/00_wine_spectra_baseline_calibration_interactive_example.ipynb)
<br />

![image](../main/images/01_example_interactive.png "Generated interactive widget based")
<br /> [Jupyter Notebook widget generator source code](../blob/main/notebooks/interactive_diagrams.ipynb)<a id="analysis-examples-interact-sc"></a>
<br />

## Contributing

<br />

## License

[MIT](https://choosealicense.com/licenses/mit/)
