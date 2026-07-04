% order5v2_1399  eq1=11222 eq2=35058  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,f(X,Z)),f(W,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(f(X,Z),Y)),Z) )).
