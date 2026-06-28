% hard3_0335  eq1=3130 eq2=2119  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(Y,X),Z),Z),X) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Z),f(W,X)) )).
