% order5_0178  eq1=30393 eq2=12347  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,f(f(Y,Z),Y))),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),W),f(X,W))) )).
