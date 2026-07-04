% order5v2_1345  eq1=39286 eq2=9539  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Y),f(X,Z)),W),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(Y,f(W,Z)))) )).
