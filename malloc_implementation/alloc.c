/**
 * Malloc
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
 
 
typedef struct _metadata_t {
  unsigned int size;     // The size of the memory block.
  unsigned char isUsed;  // 0 if the block is free; 1 if the block is used.
  struct metadatas_t *previous;
  struct metadatas_t *next;
} metadata_t;
 
metadata_t *head = NULL;
void *startOfHeap = NULL;
/**
 * Allocate space for array in memory
 *
 * Allocates a block of memory for an array of num elements, each of them size
 * bytes long, and initializes all its bits to zero. The effective result is
 * the allocation of an zero-initialized memory block of (num * size) bytes.
 *
 * @param num
 *    Number of elements to be allocated.
 * @param size
 *    Size of elements.
 *
 * @return
 *    A pointer to the memory block allocated by the function.
 *
 *    The type of this pointer is always void*, which can be cast to the
 *    desired type of data pointer in order to be dereferenceable.
 *
 *    If the function failed to allocate the requested block of memory, a
 *    NULL pointer is returned.
 *
 * @see http://www.cplusplus.com/reference/clibrary/cstdlib/calloc/
 */
void *calloc(size_t num, size_t size) {
  void *new_block = malloc(num*size);
  memset(new_block, 0, num*size);
  return new_block;
}
 
 
/**
 * Allocate memory block
 *
 * Allocates a block of size bytes of memory, returning a pointer to the
 * beginning of the block.  The content of the newly allocated block of
 * memory is not initialized, remaining with indeterminate values.
 *
 * @param size
 *    Size of the memory block, in bytes.
 *
 * @return
 *    On success, a pointer to the memory block allocated by the function.
 *
 *    The type of this pointer is always void*, which can be cast to the
 *    desired type of data pointer in order to be dereferenceable.
 *
 *    If the function failed to allocate the requested block of memory,
 *    a null pointer is returned.
 *
 * @see http://www.cplusplus.com/reference/clibrary/cstdlib/malloc/
 */
 
void *malloc(size_t size) {
  // implement malloc
  // If we have not recorded the start of the heap, record it:
  if (startOfHeap == NULL) {
    startOfHeap = sbrk(0);
    head = startOfHeap;
    // sbrk(0) returns the current end of our heap, without increasing it.
  }
  if(!size) {
    return NULL;
  }
  // Print out data about each metadata chunk:
  metadata_t *curMeta = head;
  void *endOfHeap = sbrk(0);
  // printf("-- Start of Heap (%p) --\n", startOfHeap);
  while ((void *)curMeta < endOfHeap) {   // While we're before the end of the heap...
    // printf("metadata for memory %p: (%p, size=%d, isUsed=%d)\n", (void *)curMeta + sizeof(metadata_t), curMeta, curMeta->size, curMeta->isUsed);
 
    //if the currrent block has not been used
    if (!(curMeta->isUsed)) {
      if (curMeta->size >= size) {
        size_t new_block_size = curMeta->size - size - sizeof(metadata_t);
        //if the size of availible blockis larger than needed, we split it
        if (new_block_size > 0) {
          metadata_t *new_block = (void*)curMeta + size + sizeof(metadata_t);
          new_block->isUsed = 0;
          new_block->size = new_block_size;
        }
        //else if the block and its meta data can just fit into the block with no residual
        curMeta->isUsed = 1;
        curMeta -> size = size;
        // printf("split one block");
        return (void *)curMeta + sizeof(metadata_t);  
      }
      //if current block does not have enough space, we check for the next block to see if we can do memory coalescing to get enough space
      //coalescing只查了next，没插上一个
      //malloc太大了
 
      else {
        metadata_t *next_block = (void*)curMeta + curMeta->size + sizeof(metadata_t);
        //if the next block is also availible
        if(!next_block->isUsed) {
          if (curMeta->size + next_block->size - size >= 0) {
            //mark the current block as used, and make the rest of the next block the new unused "next block"
            curMeta->size = size;
            curMeta->isUsed = 1;
 
            metadata_t *new_next_block = (void*)curMeta + curMeta->size + sizeof(metadata_t);
            new_next_block->size = curMeta->size + next_block->size - size;
            new_next_block->isUsed = 0;
            // printf("merge 2 blocks");
            return (void *)curMeta + sizeof(metadata_t);
          }
        }
      }
    }
 
    //move to te next block
    curMeta = (void *)curMeta + curMeta->size + sizeof(metadata_t);
  }
 
 
  // printf("-- End of Heap (%p) --\n\n", endOfHeap);
 
  // Allocate heap memory for the metadata structure and populate the variables:
  metadata_t *meta = sbrk( sizeof(metadata_t) );
  meta->size = size;
  meta->isUsed = 1;
 
  // Allocate heap memory for the requested memory:
  void *ptr = sbrk( meta->size );
 
  // Return the pointer for the requested memory:
  return ptr;
}
 
 
/**
 * Deallocate space in memory
 *
 * A block of memory previously allocated using a call to malloc(),
 * calloc() or realloc() is deallocated, making it available again for
 * further allocations.
 *
 * Notice that this function leaves the value of ptr unchanged, hence
 * it still points to the same (now invalid) location, and not to the
 * null pointer.
 *
 * @param ptr
 *    Pointer to a memory block previously allocated with malloc(),
 *    calloc() or realloc() to be deallocated.  If a null pointer is
 *    passed as argument, no action occurs.
 */
void free(void *ptr) {
  // implement free
  metadata_t *curMeta = ptr - sizeof(metadata_t);
  curMeta->isUsed = 0;
}
 
 
/**
 * Reallocate memory block
 *
 * The size of the memory block pointed to by the ptr parameter is changed
 * to the size bytes, expanding or reducing the amount of memory available
 * in the block.
 *
 * The function may move the memory block to a new location, in which case
 * the new location is returned. The content of the memory block is preserved
 * up to the lesser of the new and old sizes, even if the block is moved. If
 * the new size is larger, the value of the newly allocated portion is
 * indeterminate.
 *
 * In case that ptr is NULL, the function behaves exactly as malloc, assigning
 * a new block of size bytes and returning a pointer to the beginning of it.
 *
 * In case that the size is 0, the memory previously allocated in ptr is
 * deallocated as if a call to free was made, and a NULL pointer is returned.
 *
 * @param ptr
 *    Pointer to a memory block previously allocated with malloc(), calloc()
 *    or realloc() to be reallocated.
 *
 *    If this is NULL, a new block is allocated and a pointer to it is
 *    returned by the function.
 *
 * @param size
 *    New size for the memory block, in bytes.
 *
 *    If it is 0 and ptr points to an existing block of memory, the memory
 *    block pointed by ptr is deallocated and a NULL pointer is returned.
 *
 * @return
 *    A pointer to the reallocated memory block, which may be either the
 *    same as the ptr argument or a new location.
 *
 *    The type of this pointer is void*, which can be cast to the desired
 *    type of data pointer in order to be dereferenceable.
 *
 *    If the function failed to allocate the requested block of memory,
 *    a NULL pointer is returned, and the memory block pointed to by
 *    argument ptr is left unchanged.
 *
 * @see http://www.cplusplus.com/reference/clibrary/cstdlib/realloc/
 */
void *realloc(void *ptr, size_t size) {
    // implement realloc:
    if(!ptr) {
      ptr = malloc(size);
      return ptr;
    }
    if ((size == 0)) {
      free(ptr);
      return NULL;
    }
    void *new_position = malloc(size);
    if (!new_position) {
      return NULL;
    }
    else {
      memcpy(new_position, ptr, size);
      free(ptr);
    }
    return new_position;
}
