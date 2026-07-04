% order5_0036  eq1=56149 eq2=11444  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,f(Y,Z)) = f(f(Y,X),f(Y,Z)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(Y,Y)),f(Z,W))) )).
