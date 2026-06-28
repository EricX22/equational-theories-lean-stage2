% hard3_0046  eq1=294 eq2=2318  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),Y),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(X,f(Z,Z))),X) )).
