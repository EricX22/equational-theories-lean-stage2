% order5_0250  eq1=31520 eq2=940  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(Z,X),f(X,Z))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(W,Z))) )).
