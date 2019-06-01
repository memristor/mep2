#ifndef FSA_H
#define FSA_H

#include <cstring>
#include <iostream>
template <class T, int N = 100>
class FixedSizeAllocator
{
private:
	struct FSAElem {
	   T userElement;
	   FSAElem *pNext;
	};
	FSAElem *m_pFirstFree;
	int m_pMemory[(sizeof(FSAElem) * N) / sizeof(int) + 1];
	
public:
	FixedSizeAllocator(bool clear_memory = false) {
		m_pFirstFree = (FSAElem*)m_pMemory;
		if(clear_memory) memset( m_pMemory, 0, sizeof(FSAElem) * N );
		FSAElem *elem = m_pFirstFree;
		for(unsigned int i=0; i<N; i++) {
			elem->pNext = elem+1;
			elem++;
		}
		(elem-1)->pNext = NULL;
	}
	
	template<class... Args>
	T* alloc(Args&&... args) {
		FSAElem *pNewNode;
		if(!m_pFirstFree) {
			std::cout << "NULLLLL !!!!!!! " << typeid(T).name() << " " << T::ref_count << "\n";
			return NULL;
		} else {
			pNewNode = m_pFirstFree;
			new (&pNewNode->userElement) T(args...);
			m_pFirstFree = m_pFirstFree->pNext;
		}      
	   
		return reinterpret_cast<T*>(pNewNode);
	}
	
	void free(T *user_data) {
		FSAElem *pNode = reinterpret_cast<FSAElem*>(user_data);
		user_data->~T();
		pNode->pNext = m_pFirstFree;
		m_pFirstFree = pNode;
	}
};

#endif
