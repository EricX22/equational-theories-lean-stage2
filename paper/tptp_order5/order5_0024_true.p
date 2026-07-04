% order5_0024  eq1=19202 eq2=9855  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Y),f(f(Z,Z),f(W,Y))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(Y,f(Z,W)))) )).
