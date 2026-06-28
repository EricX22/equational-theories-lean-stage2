% hard3_0165  eq1=1487 eq2=232  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,X),f(X,f(Z,W))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(Y,f(Y,Y)),Y) )).
