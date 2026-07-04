% order5_0243  eq1=27657 eq2=6206  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),Z),f(X,X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Y,f(f(W,X),Y)))) )).
