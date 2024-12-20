// Before refactoring
bool utl_Vector_equals(utl_Vector* a, utl_Vector* b) {
    if (a != b) {
        if (a->size == b->size) {
            if (a->message_def != NULL && b->message_def != NULL) {
                if (a->message_def == NULL || a->message_def->type == b->message_def->type) {
                    if (a->message_def == NULL || a->message_def->type != TLOBJECT || a->message_def->sub.type_def == b->message_def->sub.type_def) {
                        for (size_t i = 0; i < a->size; i++) {
                            void* value_a = a->items[i];
                            void* value_b = a->items[i];

                            // Type-based checks
                            switch (a->message_def->type) {
                                case FLAGS:
                                case INT32: {
                                    if (((utl_Int32*)value_a)->value != ((utl_Int32*)value_b)->value)
                                        return false;
                                    break;
                                }
                                case INT64: {
                                    if (((utl_Int64*)value_a)->value != ((utl_Int64*)value_b)->value)
                                        return false;
                                    break;
                                }
                                case INT128: {
                                    char* ia = ((utl_Int128*)value_a)->value;
                                    char* ib = ((utl_Int128*)value_b)->value;
                                    if (!memcmp(ia, ib, 16))
                                        return false;
                                    break;
                                }
                                case INT256: {
                                    char* ia = ((utl_Int256*)value_a)->value;
                                    char* ib = ((utl_Int256*)value_b)->value;
                                    if (!memcmp(ia, ib, 32))
                                        return false;
                                    break;
                                }
                                case DOUBLE: {
                                    if (((utl_Double*)value_a)->value != ((utl_Double*)value_b)->value)
                                        return false;
                                    break;
                                }
                                case FULL_BOOL:
                                case BIT_BOOL: {
                                    if (((utl_Bool*)value_a)->value != ((utl_Bool*)value_b)->value)
                                        return false;
                                    break;
                                }
                                case BYTES: {
                                    if (!utl_StringView_equals(((utl_Bytes*)value_a)->value,
                                                               ((utl_Bytes*)value_b)->value))
                                        return false;
                                    break;
                                }
                                case STRING: {
                                    if (!utl_StringView_equals(((utl_Bytes*)value_a)->value,
                                                               ((utl_Bytes*)value_b)->value))
                                        return false;
                                    break;
                                }
                                case TLOBJECT: {
                                    if (!utl_Message_equals(value_a, value_b))
                                        return false;
                                    break;
                                }
                                case VECTOR: {
                                    if (!utl_Vector_equals(value_a, value_b))
                                        return false;
                                    break;
                                }
                            }
                        }
                    } else {
                        return false;
                    }
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else {
            return false;
        }
    } else {
        return true;
    }

    return true;
}

// After refactoring
bool utl_Vector_equals(utl_Vector* a, utl_Vector* b) {
    if(a == b) {
        return true;
    }
    if(a->size != b->size) {
        return false;
    }
    if(a->message_def == NULL || b->message_def == NULL) {
        return false;
    }
    if(a->message_def != NULL && a->message_def->type != b->message_def->type) {
        return false;
    }
    if(a->message_def != NULL && a->message_def->type == TLOBJECT && a->message_def->sub.type_def != b->message_def->sub.type_def) {
        return false;
    }

    for(size_t i = 0; i < a->size; i++) {
        void* value_a = a->items[i];
        void* value_b = a->items[i];

        // Type-based checks
        switch (a->message_def->type) {
            case FLAGS:
            case INT32: {
                if(((utl_Int32*)value_a)->value != ((utl_Int32*)value_b)->value)
                    return false;
                break;
            }
            case INT64: {
                if(((utl_Int64*)value_a)->value != ((utl_Int64*)value_b)->value)
                    return false;
                break;
            }
            case INT128: {
                char* ia = ((utl_Int128*)value_a)->value;
                char* ib = ((utl_Int128*)value_b)->value;
                if(!memcmp(ia, ib, 16))
                    return false;
                break;
            }
            case INT256: {
                char* ia = ((utl_Int256*)value_a)->value;
                char* ib = ((utl_Int256*)value_b)->value;
                if(!memcmp(ia, ib, 32))
                    return false;
                break;
            }
            case DOUBLE: {
                if(((utl_Double*)value_a)->value != ((utl_Double*)value_b)->value)
                    return false;
                break;
            }
            case FULL_BOOL:
            case BIT_BOOL: {
                if(((utl_Bool*)value_a)->value != ((utl_Bool*)value_b)->value)
                    return false;
                break;
            }
            case BYTES: {
                if(!utl_StringView_equals(((utl_Bytes*)value_a)->value, ((utl_Bytes*)value_b)->value))
                    return false;
                break;
            }
            case STRING: {
                if(!utl_StringView_equals(((utl_Bytes*)value_a)->value, ((utl_Bytes*)value_b)->value))
                    return false;
                break;
            }
            case TLOBJECT: {
                if(!utl_Message_equals(value_a, value_b))
                    return false;
                break;
            }
            case VECTOR: {
                if(!utl_Vector_equals(value_a, value_b))
                    return false;
                break;
            }
        }
    }

    return true;
}
