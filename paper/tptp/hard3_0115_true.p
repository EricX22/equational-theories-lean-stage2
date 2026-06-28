% hard3_0115  eq1=926 eq2=1502  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(X,X))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,X),f(Z,f(Y,X))) )).
