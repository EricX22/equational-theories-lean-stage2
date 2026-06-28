% hard3_0105  eq1=830 eq2=3327  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(X,Y),f(Z,Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(X,Z))) )).
