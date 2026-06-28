% hard3_0272  eq1=2579 eq2=2882  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Z,X),W)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,f(Y,Z)),X),X) )).
