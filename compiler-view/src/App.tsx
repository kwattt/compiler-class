import { Box,Button,Table,TableCaption,Textarea,TableContainer,Tbody,Text, Th, Thead, Tr, Input } from "@chakra-ui/react"
import { useEffect, useState } from "react"
import axios from "axios"
import './index.css'
import Tree from "react-d3-tree"
import CodeMirror from "@uiw/react-codemirror";
import { vscodeDark } from "@uiw/codemirror-theme-vscode";

type tokenMatch = {
  token: string,
  value: string,
  line: number,
  span: string
}

// convert the response data to a tree
// for example
// {
//   "ProgramNode": {
//     "children": {

const convertTree = (tree: any) => {
  // for key in dict
  const parseChildren = (children: any) : any => {
    if(
      typeof children === 'object'
    ) {
      if(
        Object.keys(children).length === 1
      ) {
        const key = Object.keys(children)[0]
        if(
          typeof children[key] === 'object'
        ) {
          return [{
            name: key,
            children: children[key] ? parseChildren(children[key]) : [{
              name: 'empty'
            }]
          }]
        } else {
          return [{
            name: children[key],
          }]
        }
      } else {
        return Object.keys(children).map((key) => {
          if(
            typeof children[key] === 'object'
          ) {
          return {
              name: key,
              children: children[key] ? parseChildren(children[key]) : [{
                name: 'empty'
              }]
            }
          } else {
            return {name:key ,children: [{name: children[key]}]}
          }
        })
      }
    } else {
      return [{}]
    }
  }

  return  parseChildren(tree)

}

const App = () => {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [tdata, setData] = useState<tokenMatch[]>([])
  const [error, setError] = useState('')
  const [treeData, setTreeData] = useState<any>({})
  const [file, setFile] = useState<File | null>(null);
  const [pseudo, setPseudo] = useState('')
  const [asm, setAsm] = useState('')

  const getAxiosData = async (sdata: string) => {
    const { data } = await axios.post('http://localhost:5000/api/v1/lexico', { code: sdata })
    
    // status 200
    
    if(data.error) {
      setOutput('')
      setData([])
      setError(data.error)
      setTreeData({})
    }
    else {
      setError('')
      setData(data.tokens)
      setOutput(data.output)
      console.log(convertTree(data.tree))
      setTreeData(convertTree(data.tree))
      setPseudo(data.pseudo)
      setAsm(data.asm)
    }

  }

  useEffect(() => {
    // update the input value
    if(file) {
      const reader = new FileReader()
      reader.readAsText(file)
      reader.onloadend = () => {
        if(reader.result) {
          setInput(reader.result.toString())
        }
      }
    }
  }, [file])

  return <body><Box h='100vh' w='100vw'
    p='2em'
  >
    <Text
    fontSize='2em'
    fontWeight='bold'
    >Compilador </Text>

    <Box>
      <Box>
        <Box display='flex' 
        my='1em'
        >
        <Text>Input</Text> 
        <Input
          w='10vw'
          // upload button
          type='file'

          onChange={(e) => {
            if (e.target.files) {
              setFile(e.target.files[0]);
            }
          }}
        >
        </Input>
        <Button 
          ml='2em' 
          size='xs' 
          colorScheme='linkedin'
          onClick={() => getAxiosData(input)}
        >Analizar</Button>
        </Box>
        <CodeMirror
          value={input}
          theme={vscodeDark}
          onChange={(e) => setInput(e)}
        ></CodeMirror>

        <Text color='red'>{error}</Text>

        <Text>Resultado {
          tdata.length > 0 ? `(${tdata.length} tokens)` : ''
          }</Text>
        <Textarea disabled
          minH='5vh'
          value={output}
          onChange={(e) => setOutput(e.target.value)}
          bg='rgba(250,250,250,0.8)'
          color='black'
        ></Textarea>
      </Box>
      
      <Box
        maxH='30vh'
        overflowY='scroll'
      >
        <TableContainer>
          <Table variant='simple'>
            <TableCaption>Tabla de simbolos</TableCaption>
            <Thead>
              <Tr>
                <Th>Token</Th>
                <th>Lexema</th>
                <th>Linea</th>
                <th>Posicion</th>
              </Tr>
            </Thead>

            <Tbody>
              {tdata.map((t, index) => {
                return <Tr
                  key={index}
                >
                  <Th>{t.token}</Th>
                  <th>{t.value}</th>
                  <th>{t.line}</th>
                  <th>{t.span}</th>
                </Tr>
              })}
            </Tbody>
            
          </Table>
        </TableContainer>
      </Box>
      <Box
        w='90vw'
      >
        <Text>Parsed Data</Text>
        <Box
        h='100vh'
        >
          <Tree 
            data={treeData}
            orientation={'vertical'}
          />
        </Box>
      </Box>
      <Box>
        <Text>generated</Text>
        <Textarea
          my='3%'
          minH='30vh'
          value={pseudo}
          onChange={(e) => setPseudo(e.target.value)}
          bg='rgba(250,250,250,0.8)'
          color='black'
        ></Textarea>
      </Box>
      <Box>
        <Text>asm</Text>
        <Textarea
          my='3%'
          minH='30vh'
          value={asm}
          onChange={(e) => setPseudo(e.target.value)}
          bg='rgba(250,250,250,0.8)'
          color='black'
        ></Textarea>
      </Box>
    </Box>
  </Box></body>
}

export default App 