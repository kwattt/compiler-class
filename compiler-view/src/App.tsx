import { Box,Button,Table,TableCaption,TableContainer,Tbody,Text, Textarea, Th, Thead, Tr } from "@chakra-ui/react"
import { useState } from "react"
import axios from "axios"

import './index.css'

type tokenMatch = {
  token: string,
  value: string,
  line: number,
  span: string
}

const App = () => {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [tdata, setData] = useState<tokenMatch[]>([])
  const [error, setError] = useState('')
  
  const getAxiosData = async (sdata: string) => {
    const { data } = await axios.post('http://localhost:5000/api/v1/lexico', { code: sdata })
    
    // status 200
    
    if(data.error) {
      setOutput('')
      setData([])
      setError(data.error)
    }
    else {
      setError('')
      setData(data.tokens)
      setOutput(data.output)
    }

    console.log(tdata)
  }

  return <body><Box h='100vh' w='100vw'
    p='2em'
  >
    <Text
    fontSize='2em'
    fontWeight='bold'
    >Analizador Lexico</Text>

    <Box>
      <Box>
        <Box display='flex' 
        my='1em'
        >
        <Text>Input</Text> 
        <Button 
          ml='2em' 
          size='xs' 
          colorScheme='linkedin'
          onClick={() => getAxiosData(input)}
        >Analizar</Button>
        </Box>
        <Textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          bg='rgba(250,250,250,0.9)'
        ></Textarea>

        <Text color='red'>{error}</Text>

        <Text>Resultado {
          tdata.length > 0 ? `(${tdata.length} tokens)` : ''
          }</Text>
        <Textarea disabled
          minH='0.5vh'
          value={output}
          onChange={(e) => setOutput(e.target.value)}
          bg='rgba(250,250,250,0.8)'
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
    </Box>
  </Box></body>
}

export default App 